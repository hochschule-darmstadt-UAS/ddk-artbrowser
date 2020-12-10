import datetime
import json
import time
import uuid
import sys
import os
from typing import List, Dict, Optional
from elasticsearch import Elasticsearch, helpers, NotFoundError

DDK_INDEX_KEY = "ddk_artbrowser"

# Increase timeout because snapshot-operations have exceeded the default timeout of 10 seconds
# This depends on the size of the indices on the elasticsearch server.
# It's easier to set an estimated value here than calculate it. The value varies within seconds.
SNAPSHOT_TIMEOUT = 40

# Some attributes on the elasticsearch have to be explicitly typed
# Otherwise the sort functionallity doesn't work (e. g. for long datatypes)
# Each property not mentioned in this Dict will be automatically mapped by elasticsearch
index_creation_body = {"mappings": {"properties": {"rank": {"type": "float"}}}}


class DDKElasticsearchClient:

    def __init__(self, es):
        self.es = es

    def create_empty_index(self, index_name: str, body: Optional[Dict] = index_creation_body) -> bool:
        """Creates an empty index (meaning no documents inside)

        Args:
            index_name: Name of the index to be created
            body: Body to be passed as parameter when creating the indices
        Returns:
            True if index didn't exist and could be created else False
        """
        if self.es.indices.exists(index=index_name):
            print("Index with the name " + index_name + " already exists")
            return False

        self.es.indices.create(index=index_name, body=index_creation_body)
        return True

    def delete_index(self, index_name: str) -> bool:
        """Delete an index by it's name

        Args:
            index_name: Name of the index to be deleted

        Returns:
            True if index extists and could be deleted else False
        """
        if self.es.indices.exists(index=index_name):
            print("Deleting index: " + index_name + " now")
            self.es.indices.delete(index_name)
            return True
        print("The index: " + index_name + "to be deleted doesn't exist")
        return False

    def load_json_to_index(self, index_name: str, filenames: List[str]) -> None:
        """Creates an index with new documents from art_ontology_<language_code>.json

        Args:
            index_name: Index name in which documents should be created
            filenames: Paths to the files which contains the documents to be created e. g. artists.json
        """
        if not self.es.indices.exists(index=index_name):
            raise NotFoundError

        print(
            'Start loading data to index "'
            + index_name
            + '" now. Current time: '
            + str(datetime.datetime.now())
        )
        start = time.time()

        # load items from filename
        total_items = 0
        for filename in filenames:
            entity_type = os.path.splitext(os.path.basename(filename))[0]   # ./data/artist.json => artist
            print("Loading " + filename)
            with open(filename, encoding="utf-8") as file:
                items = json.load(file)
                print(f"{filename} has {len(items)} items")
                print("Bulk insert starting now")
                bulk_insert = [
                    {"_index": index_name, "_id": uuid.uuid4(), "_source": json.dumps(item)}
                    for item in items
                ]
                helpers.bulk(self.es, bulk_insert)
                total_items += len(items)

        end = time.time()
        print(f"{total_items} documents were created in index {index_name}")
        print(
            f"Finished creating the index current time: {str(datetime.datetime.now())} it took {str((int((end - start) / 60)))} minutes"
        )

    def swap_index(self, index_name_new: str, index_name_current: str, index_name_old: str) -> bool:
        """Swaps the new index with the current one the current will be backed up in index_name_old
        This is possible because the backup and restore feature of elasticsearch allows renaming when restoring a snapshot

        Args:
            index_name_new: Newly created index which replaces the current index
            index_name_current: The current index which replaces the old index
            index_name_old: The old index which will be deleted

        Returns:
            True when the index swap worked else False
        """
        print("Checking if current index exists")
        # Check for newly setup ElasticSearch-Server
        if not self.es.indices.exists(index=index_name_current):
            print(
                'The current index named: "'
                + index_name_current
                + '" does not exist. It will be created now ...'
            )
            self.create_empty_index(index_name=index_name_current)
        if not self.es.indices.exists(index=index_name_new):
            print(
                'The new index named: "'
                + index_name_new
                + '" does not exist therefore the swap cannot be executed'
            )
            return False

        print("Creating snapshots from given indices to swap")
        snapshot_appendix = "_snapshot"
        index_new_snapshot = index_name_new + snapshot_appendix
        index_current_snapshot = index_name_current + snapshot_appendix
        # Snapshot the new index
        self.create_snapshot_for_index(
            index_name=index_name_new, snapshot_name=index_new_snapshot
        )
        # Snapshot the current index
        self.create_snapshot_for_index(
            index_name=index_name_current, snapshot_name=index_current_snapshot
        )
        self.list_all_snapshots_from_repository()

        # First swap
        # Check if index_name_current_old exists if it does delete index

        if self.es.indices.exists(index_name_old):
            self.es.indices.delete(index_name_old)
        # Apply snapshot to index_name_current and rename it to index_name_current_old
        self.apply_snapshot_from_repository(
            snapshot_name=index_current_snapshot,
            index_name=index_name_current,
            new_index_name=index_name_old,
        )

        # Second swap
        # Apply index_new_snapshot on index_current
        self.apply_snapshot_from_repository(
            snapshot_name=index_new_snapshot,
            index_name=index_name_new,
            new_index_name=index_name_current,
        )

        # Now the indices should be swapped
        # Cleanup
        # Remove created snapshots
        self.delete_snapshot_from_repository(snapshot_name=index_new_snapshot)
        self.delete_snapshot_from_repository(snapshot_name=index_current_snapshot)

        # Delete index_name_new
        self.delete_index(index_name_new)
        return True

    def create_snapshot_for_index(self, index_name: str, snapshot_name: str,
                                  repository_name: Optional[str] = "ddk_artbrowser_index_backup",
                                  backup_directory: Optional[str] = "/var/lib/elasticsearch/backup",
                                  ) -> None:
        """Creates a snapshot for an given index

        Args:
            index_name: Index for which the snapshot should be created for
            snapshot_name: Name for the snapshot
            repository_name: Name for a repository which stores snapshots
                                The ddk-artbrowser repository is 'ddk_artbrowser_index_backup'
            backup_directory: Directory in which the repository is located
                                The ddk-artbrowser backup directory is /var/lib/elasticsearch/backup
                                IMPORTANT:
                                1. The directory has to exist before execution
                                2. This directory is also needed in the elasticsearch.yaml configuration file
                                    - Following entry in elasticsearch.yml required:
                                    path.repo: ["path_to_folder"]
        """

        try:
            # Check if repository already was created
            self.es.snapshot.get_repository(repository_name, request_timeout=SNAPSHOT_TIMEOUT)
        except:  # If not create
            self.es.snapshot.create_repository(
                repository=repository_name,
                body={"type": "fs", "settings": {"location": backup_directory}},
                request_timeout=SNAPSHOT_TIMEOUT
            )
        if self.es.indices.exists(index=index_name):
            try:
                # Check if this snapshot was deleted if not remove it
                self.es.snapshot.get(repository=repository_name, snapshot=snapshot_name,
                                     request_timeout=SNAPSHOT_TIMEOUT)
                self.delete_snapshot_from_repository(snapshot_name)
            except:
                pass
            self.es.snapshot.create(
                repository=repository_name,
                snapshot=snapshot_name,
                body={"indices": index_name},
                params={"wait_for_completion": "true"},
                request_timeout=SNAPSHOT_TIMEOUT
            )
            print("Snapshot created: " + snapshot_name)
        else:
            print("There is no index with name: " + index_name)

    def apply_snapshot_from_repository(self, snapshot_name: str, index_name: str, new_index_name: str,
                                       repository_name: Optional[str] = "ddk_artbrowser_index_backup",
                                       ) -> None:
        """Applies a snapshot created in an earlier creation from a repository

        Args:
            index_name: Name of the index the snapshot should be applied
            repository_name: Name of the repository the snapshot is in
            snapshot_name: Name of the snapshot
        """
        try:
            self.es.indices.close(index=index_name, request_timeout=SNAPSHOT_TIMEOUT)
            result = self.es.snapshot.restore(
                repository=repository_name,
                snapshot=snapshot_name,
                body={
                    "indices": index_name,
                    "rename_pattern": index_name,
                    "rename_replacement": new_index_name,
                },
                params={"wait_for_completion": "true"},
                request_timeout=SNAPSHOT_TIMEOUT
            )
            print(str(result))
        except Exception as e:
            print(str(e))

    def delete_snapshot_from_repository(self, snapshot_name: str,
                                        repository_name: Optional[str] = "ddk_artbrowser_index_backup",
                                        backup_directory: Optional[str] = "/var/lib/elasticsearch/backup",
                                        ) -> None:
        """Delete a snapshot from the repository

        Args:
            snapshot_name: Name of the snapshot to be deleted
            repository_name: Name of the repository the snapshot is in
            backup_directory: Directory in which the repository is located
                               See create_snapshot_for_index for more information on that
        """
        try:
            # Check if repository already was created
            self.es.snapshot.get_repository(repository_name, request_timeout=SNAPSHOT_TIMEOUT)
        except:  # If not create
            self.es.snapshot.create_repository(
                repository=repository_name,
                body={"type": "fs", "settings": {"location": backup_directory}},
                request_timeout=SNAPSHOT_TIMEOUT
            )
        try:
            self.es.snapshot.delete(repository=repository_name, snapshot=snapshot_name, request_timeout=SNAPSHOT_TIMEOUT)
        except Exception as e:
            print("There was a problem deleting the snapshot:")
            print(str(e))

    def list_all_snapshots_from_repository(self, repository_name: Optional[str] = "ddk_artbrowser_index_backup") -> None:
        """Lists all created snapshots in a repository

        Args:
            repository_name: Name of the repository which contains the snapshots
        """
        try:
            for snapshot in self.es.snapshot.get(repository=repository_name, snapshot='_all'):
                print(snapshot)
        except Exception as e:
            print(str(e))

    def list_all_indices(self) -> None:
        """List all indices
        """

        try:
            for index in self.es.indices.get("*"):
                print(index)
        except Exception as e:
            print(str(e))

    def create_ddk_index(self, filepaths: List[str], first_creation=False) -> None:
        """Creates a new ddk-artbrowser index
        """
        # check if actual index is already existent, if not create it (e.g. on first run)
        if first_creation:
            new_index_name = DDK_INDEX_KEY
        else:
            new_index_name = DDK_INDEX_KEY + "_new"

        self.create_empty_index(new_index_name)
        self.load_json_to_index(new_index_name, filepaths)

    def swap_ddk_index(self) -> None:
        """Swaps a newly created index (identified by it's name *_new) with the current one
        The current index is saved to ddk_artbrowser_old
        """
        self.swap_index(
            index_name_new=DDK_INDEX_KEY + "_new",
            index_name_current=DDK_INDEX_KEY,
            index_name_old=DDK_INDEX_KEY + "_old",
        )
        # close the old index to avoid overhead. The index can be reopened any time.
        es.indices.close(DDK_INDEX_KEY + "_old")

    def swap_to_backup_for_each_language(self, delete_non_working_indices: Optional[bool] = True) -> None:
        """Can be used if the current index is not working
        This resets the index to the ddk_artbrowser_old index
        he current non working index can be saved to an index with the restoration date as name
        This is only possible once because of the renaming of the index ddk_artbrowser_old to ddk_artbrowser

        Args:
            delete_non_working_indices: If this is set to True the non working indices will be deleted
                                        For debugging purposes set to this False
        """
        es = Elasticsearch()

        not_working_index_name = DDK_INDEX_KEY + time.strftime("%Y%m%d-%H%M%S")
        es.indices.open(DDK_INDEX_KEY + "_old")  # open old index for reapplying
        if self.swap_index(
                index_name_new=DDK_INDEX_KEY + "_old",
                index_name_current=DDK_INDEX_KEY,
                index_name_old=not_working_index_name,
        ):
            if delete_non_working_indices:
                print(
                    "The not working index named "
                    + not_working_index_name
                    + " will now be deleted"
                )
                self.delete_index(not_working_index_name)
            else:
                print(
                    "The not working index "
                    + DDK_INDEX_KEY
                    + " was renamed to "
                    + not_working_index_name
                    + " and can now be debugged"
                )
                print(
                    "After debugging deletion is possible with the delete_index function"
                )

    def count_check_ddk_index(self, filepaths: List[str]) -> bool:
        """After the indices were created check that the indice document count
        equals the JSON object count of the corresponding JSON file
        The corresponding JSON file is located within the filepath parameters path

        Args:
            lang_leys: Languagekeys for which the check has to be satisfied.
            filepath: Location of the art_ontology_*.json language files.
        """
        # Refresh is needed because the index stats aren't always up-to-date
        self.es.indices.refresh(DDK_INDEX_KEY)
        es_document_count_dict = self.es.cat.count(index=DDK_INDEX_KEY, params={"format": "json"})
        es_document_count = int(es_document_count_dict[0]["count"])

        total_count = 0
        for filename in filepaths:
            with open(filename, encoding="utf-8") as input:
                object_array = json.load(input)
                json_object_count = len(object_array)
                total_count += json_object_count

        if es_document_count != total_count:
            print(
                'There is a problem with the index "'
                + DDK_INDEX_KEY
                + '" the json'
                + " object count doesn't equal the document count in the index"
                + " which should be the case"
            )
        else:
            print("The index " + DDK_INDEX_KEY + " seems to be created correctly")


if __name__ == "__main__":
    json_files = []

    if len(sys.argv) < 2:
        print("usage: {} [dir/with/jsons | file1.json file2.json ...]\n".format(sys.argv[0]))
        exit(1)
    elif len(sys.argv) == 2:
        # check if argument is directory or file and handle accordingly
        path = sys.argv[1]
        if os.path.isdir(path):
            if path.endswith("/"):
                path = path[:-1]
            json_files = ["{}/{}".format(path, file) for file in os.listdir(path) if file.endswith('.json')]
        else:
            json_files = [path]
    else:
        # if more than one argument is passed, handle them all like files
        json_files = sys.argv[1:]

    print("Using {} to up upload".format(",".join(json_files)))

    es = Elasticsearch()
    ddkESClient = DDKElasticsearchClient(es)

    first_creation = not es.indices.exists(DDK_INDEX_KEY)
    print("First Creation: ", first_creation)

    ddkESClient.create_ddk_index(json_files, first_creation)
    if not first_creation:
        ddkESClient.swap_ddk_index()
    ddkESClient.count_check_ddk_index(json_files)

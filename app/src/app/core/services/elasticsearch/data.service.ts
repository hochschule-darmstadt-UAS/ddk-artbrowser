import * as _ from 'lodash';
import { HttpClient } from '@angular/common/http';
import { Inject, Injectable, LOCALE_ID } from '@angular/core';
import { ArtSearch, Artwork, Entity, EntityIcon, EntityType } from 'src/app/shared/models/models';
import { environment } from 'src/environments/environment';
import { usePlural } from 'src/app/shared/models/entity.interface';
import * as bodyBuilder from 'bodybuilder';
import { Bodybuilder } from 'bodybuilder';
import { image, imageMedium, imageSmall } from '../ddk.service';

const defaultSortField = 'rank';

/**
 * Service that handles the requests to the API
 */
@Injectable()
export class DataService {
  /** base url of elasticSearch server */
  private readonly searchEndPoint: string;
  private readonly countEndPoint: string;
  private readonly ISO_639_1_LOCALE: string;
  private indexName: string;

  /**
   * Constructor
   */
  constructor(private http: HttpClient, @Inject(LOCALE_ID) localeId: string) {
    // build backend api url with specific index by localeId
    this.ISO_639_1_LOCALE = localeId.substr(0, 2);
    this.searchEndPoint = environment.elasticBase + '/_search';
    this.countEndPoint = environment.elasticBase + '/_count';
    this.indexName = 'ddk_artbrowser';
  }

  /**
   * set type specific attributes
   * @param entity entity object
   */
  private static setTypes(entity: any) {
    if (entity.entityType && entity.id) {
      entity.route = `/${entity.entityType}/${entity.id}`;
      entity.icon = EntityIcon[entity.entityType.toUpperCase()];
    }
  }

  /**
   * Fetches an entity from the server
   * Returns null if not found
   * @param id Id of the entity to retrieve
   * @param type if specified, it is assured that the returned entity has this entityType
   */
  public async findById<T>(id: string, type?: EntityType): Promise<T> {
    const body = bodyBuilder()
      .query('match', 'id', id);
    const entities = await this.performQuery<T>(body, this.searchEndPoint, type);
    return !entities.length ? null : entities[0];
  }

  /**
   * Fetches multiple entities from the server
   * @param ids ids of entities that should be retrieved
   * @param type if specified, it is assured that the returned entities have this entityType
   */
  public async findMultipleById<T>(ids: string[], type?: EntityType): Promise<T[]> {
    const copyids = ids && ids.filter(id => !!id);
    if (!copyids || copyids.length === 0) {
      return [];
    }
    const body = bodyBuilder().size(400);
    _.each(ids, id => body.orQuery('match', 'id', id));
    return this.performQuery<T>(body, this.searchEndPoint, type);
  }

  /**
   * Find Artworks by the given ids for the given type
   * @param type the type to search in
   * @param ids the ids to search for
   * @param count the number of items returned
   */
  public findArtworksByType(type: EntityType, ids: string[], count = 200): Promise<Artwork[]> {
    const body = bodyBuilder()
      .size(count)
      .sort(defaultSortField, 'desc')
      .queryMinimumShouldMatch(1, true)
      .query('match', 'entityType', EntityType.ARTWORK)
      .query('prefix', 'resources.linkResource', 'http');
    _.each(ids, id => body.orQuery('match', usePlural(type), id));
    return this.performQuery<Artwork>(body);
  }

    /**
   * Fetches all child artworks of a specified iconclass
   * Returns null if not found
   * @param iconlass with '*' to fetch all artworks which start with the specified iconclass
   * @param type if specified, it is assured that the returned entity has this entityType
   */
  public async findChildArtworksByIconography(iconclass: string, type?: EntityType): Promise<Artwork[]> {
    const body = bodyBuilder()
      .size(400)
      .sort(defaultSortField, 'desc')
      .query('match', 'entityType', EntityType.ARTWORK)
      .query('regexp', 'iconographies', {
        value: iconclass + '.*',
        flags: 'ALL',
        case_insensitive: true
      });
    let entities = await this.performQuery<Artwork>(body);

    /** Remove artwork if it belongs to the current iconclass - only return child iconclass-artworks*/
    entities = entities.filter(artwork => {
      return !artwork.iconographies.find(iconography => iconography === iconclass);
    });
    return entities;
  }

  /**
   * Find an artwork by label
   * @param label artwork label
   */
  public findArtworksByLabel(label: string): Promise<Artwork[]> {
    const body = bodyBuilder()
      .size(20)
      .sort(defaultSortField, 'desc')
      .query('match', 'entityType', EntityType.ARTWORK)
      .orQuery('match', 'label', label);
    return this.performQuery<Artwork>(body);
  }

  /**
   * Find an artwork by movement
   * @param movement label of movement
   */
  public findArtworksByMovement(movement: string): Promise<Artwork[]> {
    const body = bodyBuilder()
      .size(5)
      .sort(defaultSortField, 'desc')
      .query('match', 'entityType', EntityType.ARTWORK)
      .query('match', usePlural(EntityType.MOVEMENT), movement);
    return this.performQuery<Artwork>(body);
  }

  /**
   * Returns the artworks that contain all the given arguments.
   * @param searchObj the arguments to search for.
   * @param keywords the list of words to search for.
   */
  public searchArtworks(searchObj: ArtSearch, keywords: string[] = []): Promise<Artwork[]> {
    const body = bodyBuilder()
      .size(400)
      .sort(defaultSortField, 'desc');
    _.each(searchObj, (arr, key) => {
      if (Array.isArray(arr)) {
        _.each(arr, val => body.query('match', key, val));
      }
    });
    _.each(keywords, keyword =>
      body.query('bool', (q) => {
        return q.orQuery('match', 'label', keyword);
        // .orQuery('match', 'description', keyword);
      })
    );
    return this.performQuery(body);
  }

  public async getEntityItems<T>(type: EntityType, count = 20, from = 0): Promise<T[]> {
    const body = bodyBuilder()
      .query('match', 'entityType', type)
      .sort(defaultSortField, 'desc')
      .size(count)
      .from(from);
    return this.performQuery<T>(body);
  }

  public async countEntityItems<T>(type: EntityType) {
    const response: any = await this.http
      .get(this.countEndPoint + '?q=entityType:' + type)
      .toPromise();
    return response.count;
  }

  /**
   * Find any object in the index by the field label with the given label
   * @param label object label
   */
  public findByLabel(label: string): Promise<any[]> {
    const body = bodyBuilder()
      .orQuery('match', 'label', label)
      .orQuery('wildcard', 'label', '*' + label + '*')
      .sort(defaultSortField, 'desc')
      .size(200);
    return this.performQuery(body);
  }

  /**
   * Return 20 items for an specific category.
   * @param type category type
   * @param count size of return set
   */
  public async getCategoryItems<T>(type: EntityType, count = 20): Promise<T[]> {
    const body = bodyBuilder()
      .query('match', 'entityType', type)
      .sort(defaultSortField, 'desc')
      .size(count);
    return this.performQuery(body);
  }

  /**
   * Perform an ajax request and filter response
   * @param query elasticsearch query as body
   * @param url endpoint
   * @param type type to filter for
   */
  private async performQuery<T>(query: Bodybuilder, url: string = this.searchEndPoint, type?: EntityType) {
    const response = await this.http.post<T>(url, query.build()).toPromise();
    const entities = await this.filterData<T>(response, type);
    // set type specific attributes
    entities.forEach(entity => this.setTypes(entity));

    if (!entities.length) {
      console.warn(NoResultsWarning(query));
    }
    return entities;
  }

  /**
   * filters the data that is fetched from the server
   * @param data Elasticsearch Data
   * @param filterBy optional: type of entities that should be filtered
   */
  private async filterData<T>(data: any, filterBy?: EntityType): Promise<T[]> {
    const entities: any = [];
    data.hits.hits.forEach((val) => {
      if ((!val._index || val._index === this.indexName)
        && (!filterBy || (filterBy && val._source.entityType === filterBy))
        && (val._source.entityType !== EntityType.ARTWORK || val._source.resources.length)) {
        entities.push(this.addThumbnails(val._source));
      }
    });
    return await Promise.all(entities);
  }

  /**
   * fills entity fields imageSmall and imageMedium
   * @param entity entity for which thumbnails should be added
   */
  private async addThumbnails(entity: Entity) {
    let e;
    if (entity.entityType === EntityType.ARTWORK) {
      e = entity as Artwork;
      (entity as Artwork).resources.map(res => {
        res.image = image(res.linkResource);
        res.imageMedium = imageMedium(res.linkResource);
        res.imageSmall = imageSmall(res.linkResource);
      });
      entity.image = e.resources[0].image;
      entity.imageMedium = e.resources[0].imageMedium;
      entity.imageSmall = e.resources[0].imageSmall;
    } else {
      await this.findArtworksByType(entity.entityType, [entity.id], 1).then((result) => {
        if (result.length) {
          e = result[0];
          entity.image = e.resources[0].image;
          entity.imageMedium = e.resources[0].imageMedium;
          entity.imageSmall = e.resources[0].imageSmall;
        }
      });
    }
    return entity;
  }

  /**
   * set type specific attributes
   * @param entity entity object
   */
  private setTypes(entity: any) {
    if (entity.entityType && entity.id) {
      entity.route = `/${entity.entityType}/${entity.id}`;
      entity.icon = EntityIcon[entity.entityType.toUpperCase()];
    }
  }
}

const NoResultsWarning = query => `
The performed es-query did not yield any results. This might result in strange behavior in the application.

If you encounter any such issues please consider opening a bug report: https://github.com/hochschule-darmstadt/openartbrowser/issues/new?assignees=&labels=&template=bug_report.md&title=

Query: ${JSON.stringify(query.build())}
`;

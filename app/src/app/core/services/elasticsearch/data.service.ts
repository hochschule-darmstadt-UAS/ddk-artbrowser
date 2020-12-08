import * as _ from 'lodash';
import { HttpClient } from '@angular/common/http';
import { Inject, Injectable, LOCALE_ID } from '@angular/core';
import { ArtSearch, Artwork, Entity, EntityIcon, EntityType, Iconclass } from 'src/app/shared/models/models';
import { elasticEnvironment } from 'src/environments/environment';
import QueryBuilder from './query.builder';
import { usePlural } from '../../../shared/models/entity.interface';
import * as bodyBuilder from 'bodybuilder';

const defaultSortField = 'rank';

/**
 * Service that handles the requests to the API
 */
@Injectable()
export class DataService {
  /** base url of elasticSearch server */
  private readonly baseUrl: string;
  private readonly ISO_639_1_LOCALE: string;

  private bodybuilder = bodyBuilder();

  constructor(private http: HttpClient, @Inject(LOCALE_ID) localeId: string) {
    // build backend api url with specific index by localeId
    this.ISO_639_1_LOCALE = localeId.substr(0, 2);
    this.baseUrl = elasticEnvironment.serverURI + '/_search';
  }

  /**
   * set type specific attributes
   * @param entity entity object
   */
  private static setTypes(entity: any) {
    if (entity.type && entity.id) {
      entity.route = `/${entity.type}/${entity.id}`;
      entity.icon = EntityIcon[entity.type.toUpperCase()];
    }
  }

  public async findById<T>(id: string, type?: EntityType): Promise<T> {
    const body = bodyBuilder()
      .query('match', 'id', id)
      .build();
    const response = await this.http.post<T>(this.baseUrl, body).toPromise();
    const entities = this.filterData<T>(response, type);
    // set type specific attributes
    entities.forEach(entity => DataService.setTypes(entity));
    console.log(entities);
    return !entities.length ? null : entities[0];
  }

  public async findMultipleById<T>(ids: string[], type?: EntityType): Promise<T[]> {}

  /**
   * Find Artworks by the given ids for the given type
   * @param type the type to search in
   * @param ids the ids to search for
   */
  public findArtworksByType(type: EntityType, ids: string[], count = 200): Promise<Artwork[]> {
    const body = bodyBuilder()
      .query()
      .size(count)
      .sort(defaultSortField)
      .minimumShouldMatch(1)
      .ofType(EntityType.ARTWORK);
    ids.forEach(id => query.shouldMatch(type !== EntityType.LOCATION ? usePlural(type) : type, `${id}`));
    return this.performQuery<Artwork>(query);
  }

  public getHasPartMovements(topMovementId: string): Promise<Movement[]> {}

  public getPartOfMovements(subMovementId: string): Promise<Movement[]> {}

  public findArtworksByLabel(label: string): Promise<Artwork[]> {}

  public findArtworksByMovement(movement: string): Promise<Artwork[]> {}

  public searchArtworks(searchObj: ArtSearch, keywords: string[] = []): Promise<Artwork[]> {}

  public async getEntityItems<T>(type: EntityType, count = 20, from = 0): Promise<T[]> {}

  public async getRandomMovementArtwork<T>(movementId: string, count = 20): Promise<T[]> {}

  public findByLabel(label: string): Promise<any[]> {}

  public async getCategoryItems<T>(type: EntityType, count = 20): Promise<T[]> {}

  /**
   * filters the data that is fetched from the server
   * @param data Elasticsearch Data
   * @param filterBy optional: type of entities that should be filtered
   */
  private filterData<T>(data: any, filterBy?: EntityType): T[] {
    const entities: T[] = [];
    _.each(
      data.hits.hits,
      function(val) {
        if (!filterBy || (filterBy && val._source.type === filterBy)) {
          entities.push(this.addThumbnails(val._source));
        }
      }.bind(this)
    );
    return entities;
  }

  private addThumbnails(entity: Entity) {
    return entity;
  }
}

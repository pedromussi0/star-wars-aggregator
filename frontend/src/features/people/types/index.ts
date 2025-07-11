export interface Person {
  url: string;
  name: string;
  height: string;
  mass: string;
  gender: string;
}

interface RelatedEntity {
  url: string;
  name?: string;
  title?: string;
}

export interface PersonDetails extends Person {
  homeworld?: RelatedEntity;
  films: RelatedEntity[];
  species: RelatedEntity[];
  vehicles: RelatedEntity[];
  starships: RelatedEntity[];
} 
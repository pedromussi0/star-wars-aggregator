import {
  type SearchResultItem,
  type PersonResult,
  type FilmResult,
  type PlanetResult,
  type SpeciesResult,
  type StarshipResult,
  type VehicleResult,
} from '../types';

const PersonCard = ({ item }: { item: PersonResult }) => (
  <div>
    <p className="font-bold">{item.name}</p>
    <p className="text-sm">Gender: {item.gender}, Born: {item.birth_year}</p>
  </div>
);

const FilmCard = ({ item }: { item: FilmResult }) => (
  <div>
    <p className="font-bold">{item.title}</p>
    <p className="text-sm">Episode {item.episode_id} | Director: {item.director}</p>
  </div>
);

const PlanetCard = ({ item }: { item: PlanetResult }) => (
  <div>
    <p className="font-bold">{item.name}</p>
    <p className="text-sm">Climate: {item.climate}, Population: {item.population}</p>
  </div>
);

const SpeciesCard = ({ item }: { item: SpeciesResult }) => (
  <div>
    <p className="font-bold">{item.name}</p>
    <p className="text-sm">Classification: {item.classification}, Language: {item.language}</p>
  </div>
);

const StarshipCard = ({ item }: { item: StarshipResult }) => (
  <div>
    <p className="font-bold">{item.name}</p>
    <p className="text-sm">Model: {item.model}, Class: {item.starship_class}</p>
  </div>
);

const VehicleCard = ({ item }: { item: VehicleResult }) => (
  <div>
    <p className="font-bold">{item.name}</p>
    <p className="text-sm">Model: {item.model}, Class: {item.vehicle_class}</p>
  </div>
);

export const SearchResultItemCard = ({ item }: { item: SearchResultItem }) => {
  const renderCard = () => {
    switch (item.type) {
      case 'people':
        return <PersonCard item={item} />;
      case 'films':
        return <FilmCard item={item} />;
      case 'planets':
        return <PlanetCard item={item} />;
      case 'species':
        return <SpeciesCard item={item} />;
      case 'starships':
        return <StarshipCard item={item} />;
      case 'vehicles':
        return <VehicleCard item={item} />;
      default:
        return <p>Unsupported result type</p>;
    }
  };

  return (
    <li className="border-b p-3 hover:bg-gray-50 last:border-b-0">
      <div className="flex justify-between items-center">
        {renderCard()}
        <span className="text-xs font-mono bg-gray-200 text-gray-700 px-2 py-1 rounded capitalize">
          {item.type}
        </span>
      </div>
    </li>
  );
};
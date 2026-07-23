import Hero from '../components/Hero/Hero';
import SearchBar from '../components/SearchBar/SearchBar';
import FeatureCards from '../components/FeatureCards/FeatureCards';

function Home() {
  return (
    <>
      {/* TODO: Assemble personalized public landing modules based on user region and intent. */}
      <Hero />
      <SearchBar />
      <FeatureCards />
    </>
  );
}

export default Home;

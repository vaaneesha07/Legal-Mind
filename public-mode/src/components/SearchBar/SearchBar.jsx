import { Search } from 'lucide-react';
import './SearchBar.css';

function SearchBar() {
  return (
    <section className="search-bar-section">
      {/* TODO: Connect this input to AI-assisted legal search and suggestions. */}
      <div className="container">
        <form className="search-bar" role="search" onSubmit={(event) => event.preventDefault()}>
          <Search size={18} />
          <input type="text" placeholder="Search laws, rights, procedures..." aria-label="Search" />
          <button type="submit">Search</button>
        </form>
      </div>
    </section>
  );
}

export default SearchBar;

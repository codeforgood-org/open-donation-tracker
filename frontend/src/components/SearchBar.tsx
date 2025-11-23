import React, { useState, useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import api from '../lib/api';

interface SearchResult {
  id: number;
  type: string;
  title: string;
  description?: string;
  url: string;
  relevance_score?: number;
}

interface AutocompleteResult {
  id: number;
  type: string;
  name: string;
}

export const SearchBar: React.FC = () => {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const searchRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  // Autocomplete query
  const { data: autocompleteResults } = useQuery<AutocompleteResult[]>({
    queryKey: ['autocomplete', query],
    queryFn: async () => {
      if (query.length < 2) return [];
      const response = await api.get(`/search/autocomplete?q=${encodeURIComponent(query)}`);
      return response.data;
    },
    enabled: query.length >= 2,
  });

  // Global search query
  const { data: searchResults, refetch: searchRefetch } = useQuery<SearchResult[]>({
    queryKey: ['search', query],
    queryFn: async () => {
      if (query.length < 3) return [];
      const response = await api.get(`/search?q=${encodeURIComponent(query)}`);
      return response.data;
    },
    enabled: false, // Only run on explicit search
  });

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchRef.current && !searchRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    const results = autocompleteResults || [];

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[selectedIndex]) {
        handleResultClick(results[selectedIndex]);
      } else {
        handleSearch();
      }
    } else if (e.key === 'Escape') {
      setIsOpen(false);
    }
  };

  const handleSearch = () => {
    if (query.length >= 3) {
      searchRefetch();
      navigate(`/search?q=${encodeURIComponent(query)}`);
      setIsOpen(false);
    }
  };

  const handleResultClick = (result: AutocompleteResult) => {
    setQuery('');
    setIsOpen(false);

    // Navigate based on result type
    if (result.type === 'organization') {
      navigate(`/organizations/${result.id}`);
    } else if (result.type === 'campaign') {
      navigate(`/campaigns/${result.id}`);
    }
  };

  const handleInputChange = (value: string) => {
    setQuery(value);
    setIsOpen(value.length >= 2);
    setSelectedIndex(0);
  };

  return (
    <div ref={searchRef} className="relative w-full max-w-2xl">
      {/* Search Input */}
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => handleInputChange(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => query.length >= 2 && setIsOpen(true)}
          placeholder="Search organizations, campaigns..."
          className="w-full px-4 py-2 pl-10 pr-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <svg
          className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        {query && (
          <button
            onClick={() => {
              setQuery('');
              setIsOpen(false);
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
          >
            ✕
          </button>
        )}
      </div>

      {/* Autocomplete Dropdown */}
      {isOpen && autocompleteResults && autocompleteResults.length > 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-gray-200 max-h-96 overflow-y-auto">
          {autocompleteResults.map((result, index) => (
            <button
              key={`${result.type}-${result.id}`}
              onClick={() => handleResultClick(result)}
              className={`w-full text-left px-4 py-3 hover:bg-gray-50 transition-colors ${
                index === selectedIndex ? 'bg-blue-50' : ''
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className="flex-shrink-0">
                  {result.type === 'organization' ? (
                    <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                      🏢
                    </div>
                  ) : (
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      🎯
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-800 truncate">
                    {result.name}
                  </p>
                  <p className="text-xs text-gray-500 capitalize">
                    {result.type}
                  </p>
                </div>
              </div>
            </button>
          ))}

          {/* Show all results button */}
          <button
            onClick={handleSearch}
            className="w-full px-4 py-3 text-center text-sm text-blue-600 hover:bg-blue-50 border-t"
          >
            See all results for "{query}"
          </button>
        </div>
      )}

      {/* No results message */}
      {isOpen && query.length >= 2 && autocompleteResults?.length === 0 && (
        <div className="absolute z-50 w-full mt-2 bg-white rounded-lg shadow-xl border border-gray-200 p-4 text-center text-gray-500">
          No results found for "{query}"
        </div>
      )}
    </div>
  );
};

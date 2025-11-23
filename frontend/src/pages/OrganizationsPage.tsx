import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Shield, Star } from 'lucide-react';
import { organizationsApi } from '@/services/api';

const OrganizationsPage = () => {
  const [category, setCategory] = useState<string>('');
  const [verifiedOnly, setVerifiedOnly] = useState(true);

  const { data: organizations, isLoading } = useQuery({
    queryKey: ['organizations', category, verifiedOnly],
    queryFn: () =>
      organizationsApi.getAll({
        category: category || undefined,
        verified_only: verifiedOnly,
      }),
  });

  const categories = [
    'Education',
    'Healthcare',
    'Environment',
    'Water & Sanitation',
    'Poverty Relief',
    'Disaster Relief',
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Organizations</h1>
        <p className="text-gray-600 mt-2">
          Discover verified organizations making a difference
        </p>
      </div>

      {/* Filters */}
      <div className="card p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">Category</label>
            <select
              className="input"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center">
            <input
              type="checkbox"
              id="verified"
              checked={verifiedOnly}
              onChange={(e) => setVerifiedOnly(e.target.checked)}
              className="h-4 w-4 text-primary-600 rounded"
            />
            <label htmlFor="verified" className="ml-2 text-sm text-gray-700">
              Show verified organizations only
            </label>
          </div>
        </div>
      </div>

      {/* Organizations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {organizations && organizations.length > 0 ? (
          organizations.map((org) => (
            <Link
              key={org.id}
              to={`/organizations/${org.id}`}
              className="card p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">
                    {org.name}
                  </h3>
                  {org.category && (
                    <span className="inline-block px-2 py-1 text-xs font-medium bg-primary-100 text-primary-700 rounded">
                      {org.category}
                    </span>
                  )}
                </div>
                {org.is_verified && (
                  <Shield className="h-6 w-6 text-green-600" />
                )}
              </div>

              <p className="text-gray-600 mb-4 line-clamp-3">
                {org.description || 'No description available'}
              </p>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <Star className="h-5 w-5 text-yellow-400 fill-current" />
                  <span className="ml-1 text-sm font-medium">
                    {org.transparency_score.toFixed(1)}
                  </span>
                  <span className="ml-1 text-sm text-gray-500">
                    Transparency Score
                  </span>
                </div>
              </div>
            </Link>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">No organizations found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default OrganizationsPage;

import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { Calendar, Target } from 'lucide-react';
import { campaignsApi } from '@/services/api';
import { formatCurrency, formatDate } from '@/utils/formatters';

const CampaignsPage = () => {
  const [activeOnly, setActiveOnly] = useState(true);

  const { data: campaigns, isLoading } = useQuery({
    queryKey: ['campaigns', activeOnly],
    queryFn: () => campaignsApi.getAll({ active_only: activeOnly }),
  });

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
        <h1 className="text-3xl font-bold text-gray-900">Campaigns</h1>
        <p className="text-gray-600 mt-2">
          Support fundraising campaigns making a real impact
        </p>
      </div>

      {/* Filter */}
      <div className="card p-6 mb-8">
        <div className="flex items-center">
          <input
            type="checkbox"
            id="active"
            checked={activeOnly}
            onChange={(e) => setActiveOnly(e.target.checked)}
            className="h-4 w-4 text-primary-600 rounded"
          />
          <label htmlFor="active" className="ml-2 text-sm text-gray-700">
            Show active campaigns only
          </label>
        </div>
      </div>

      {/* Campaigns Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {campaigns && campaigns.length > 0 ? (
          campaigns.map((campaign) => {
            const percentage = (campaign.current_amount / campaign.goal_amount) * 100;
            const daysLeft = Math.max(
              0,
              Math.ceil(
                (new Date(campaign.end_date).getTime() - new Date().getTime()) /
                  (1000 * 60 * 60 * 24)
              )
            );

            return (
              <Link
                key={campaign.id}
                to={`/campaigns/${campaign.id}`}
                className="card p-6 hover:shadow-lg transition-shadow"
              >
                {campaign.image_url && (
                  <img
                    src={campaign.image_url}
                    alt={campaign.name}
                    className="w-full h-48 object-cover rounded-lg mb-4"
                  />
                )}

                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {campaign.name}
                </h3>

                <p className="text-gray-600 mb-4 line-clamp-3">
                  {campaign.description}
                </p>

                <div className="mb-4">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">Progress</span>
                    <span className="font-medium">
                      {formatCurrency(campaign.current_amount)} of{' '}
                      {formatCurrency(campaign.goal_amount)}
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div
                      className="bg-primary-600 h-2.5 rounded-full transition-all"
                      style={{ width: `${Math.min(percentage, 100)}%` }}
                    />
                  </div>
                  <div className="text-sm text-gray-600 mt-1">
                    {percentage.toFixed(1)}% funded
                  </div>
                </div>

                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-gray-600">
                    <Calendar className="h-4 w-4 mr-1" />
                    <span>
                      {campaign.is_active ? `${daysLeft} days left` : 'Ended'}
                    </span>
                  </div>
                  <div className="flex items-center text-gray-600">
                    <Target className="h-4 w-4 mr-1" />
                    <span>{formatCurrency(campaign.goal_amount)}</span>
                  </div>
                </div>
              </Link>
            );
          })
        ) : (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">No campaigns found</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default CampaignsPage;

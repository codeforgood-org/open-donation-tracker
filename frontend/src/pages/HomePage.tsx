import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Heart, TrendingUp, Shield, Users } from 'lucide-react';
import { organizationsApi, campaignsApi, donationsApi } from '@/services/api';
import { formatCurrency } from '@/utils/formatters';

const HomePage = () => {
  const { data: organizations } = useQuery({
    queryKey: ['organizations', 'verified'],
    queryFn: () => organizationsApi.getAll({ verified_only: true }),
  });

  const { data: campaigns } = useQuery({
    queryKey: ['campaigns', 'active'],
    queryFn: () => campaignsApi.getAll({ active_only: true }),
  });

  const { data: stats } = useQuery({
    queryKey: ['donation-stats'],
    queryFn: () => donationsApi.getStats(),
  });

  return (
    <div className="bg-white">
      {/* Hero Section */}
      <div className="relative bg-gradient-to-r from-primary-600 to-primary-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Track Your Impact,
              <br />
              Support with Transparency
            </h1>
            <p className="text-xl text-primary-100 mb-8 max-w-2xl mx-auto">
              Discover verified organizations, support meaningful campaigns, and
              visualize the real-world impact of your charitable donations.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/organizations" className="btn-primary bg-white text-primary-600 hover:bg-gray-100">
                Explore Organizations
              </Link>
              <Link to="/campaigns" className="btn-secondary bg-primary-700 text-white hover:bg-primary-600">
                View Campaigns
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Why Choose Open Donation Tracker?
            </h2>
            <p className="text-lg text-gray-600">
              Transparency, accountability, and impact visualization
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <Shield className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Verified Organizations</h3>
              <p className="text-gray-600">
                All organizations are verified for legitimacy and transparency
              </p>
            </div>

            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <TrendingUp className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Track Your Impact</h3>
              <p className="text-gray-600">
                See exactly how your donations are making a difference
              </p>
            </div>

            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <Heart className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Support Campaigns</h3>
              <p className="text-gray-600">
                Contribute to specific campaigns and watch progress in real-time
              </p>
            </div>

            <div className="text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <Users className="h-8 w-8 text-primary-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Join Community</h3>
              <p className="text-gray-600">
                Be part of a transparent and accountable giving community
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      {stats && (
        <div className="py-16 bg-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="text-center">
                <p className="text-4xl font-bold text-primary-600">
                  {formatCurrency(stats.total_amount)}
                </p>
                <p className="text-lg text-gray-600 mt-2">Total Donations</p>
              </div>
              <div className="text-center">
                <p className="text-4xl font-bold text-primary-600">
                  {stats.donation_count}
                </p>
                <p className="text-lg text-gray-600 mt-2">Donations Made</p>
              </div>
              <div className="text-center">
                <p className="text-4xl font-bold text-primary-600">
                  {organizations?.length || 0}
                </p>
                <p className="text-lg text-gray-600 mt-2">Verified Organizations</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Featured Campaigns */}
      {campaigns && campaigns.length > 0 && (
        <div className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Featured Campaigns
              </h2>
              <p className="text-lg text-gray-600">
                Support these active campaigns today
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              {campaigns.slice(0, 3).map((campaign) => {
                const percentage = (campaign.current_amount / campaign.goal_amount) * 100;
                return (
                  <div key={campaign.id} className="card p-6">
                    <h3 className="text-xl font-semibold mb-2">{campaign.name}</h3>
                    <p className="text-gray-600 mb-4 line-clamp-2">
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
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-primary-600 h-2 rounded-full transition-all"
                          style={{ width: `${Math.min(percentage, 100)}%` }}
                        />
                      </div>
                    </div>
                    <Link
                      to={`/campaigns/${campaign.id}`}
                      className="btn-primary w-full text-center"
                    >
                      View Campaign
                    </Link>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* CTA Section */}
      <div className="py-16 bg-primary-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white mb-4">
            Ready to Make a Difference?
          </h2>
          <p className="text-xl text-primary-100 mb-8">
            Join thousands of donors making transparent, impactful contributions
          </p>
          <Link to="/register" className="btn-primary bg-white text-primary-600 hover:bg-gray-100">
            Get Started Today
          </Link>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

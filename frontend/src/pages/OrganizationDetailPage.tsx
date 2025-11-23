import { useParams, Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Shield, Mail, Phone, Globe, DollarSign, Users, TrendingUp } from 'lucide-react';
import { organizationsApi, campaignsApi, impactReportsApi } from '@/services/api';
import { formatCurrency } from '@/utils/formatters';
import StatsCard from '@/components/StatsCard';

const OrganizationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const orgId = parseInt(id || '0');

  const { data: organization, isLoading: orgLoading } = useQuery({
    queryKey: ['organization', orgId],
    queryFn: () => organizationsApi.getById(orgId),
  });

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['organization-stats', orgId],
    queryFn: () => organizationsApi.getStats(orgId),
  });

  const { data: campaigns } = useQuery({
    queryKey: ['organization-campaigns', orgId],
    queryFn: () => campaignsApi.getAll({ organization_id: orgId }),
  });

  const { data: impactReports } = useQuery({
    queryKey: ['organization-impact', orgId],
    queryFn: () => impactReportsApi.getAll(orgId),
  });

  if (orgLoading || statsLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!organization) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Organization not found</p>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="card p-8 mb-8">
        <div className="flex items-start justify-between mb-4">
          <div>
            <div className="flex items-center space-x-2 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{organization.name}</h1>
              {organization.is_verified && (
                <Shield className="h-8 w-8 text-green-600" title="Verified" />
              )}
            </div>
            {organization.category && (
              <span className="inline-block px-3 py-1 text-sm font-medium bg-primary-100 text-primary-700 rounded">
                {organization.category}
              </span>
            )}
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-primary-600">
              {organization.transparency_score.toFixed(1)}
            </div>
            <div className="text-sm text-gray-600">Transparency Score</div>
          </div>
        </div>

        <p className="text-gray-600 mb-6">{organization.description}</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          {organization.website && (
            <div className="flex items-center space-x-2 text-gray-600">
              <Globe className="h-5 w-5" />
              <a
                href={organization.website}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:underline"
              >
                Website
              </a>
            </div>
          )}
          {organization.email && (
            <div className="flex items-center space-x-2 text-gray-600">
              <Mail className="h-5 w-5" />
              <a href={`mailto:${organization.email}`} className="text-primary-600 hover:underline">
                {organization.email}
              </a>
            </div>
          )}
          {organization.phone && (
            <div className="flex items-center space-x-2 text-gray-600">
              <Phone className="h-5 w-5" />
              <span>{organization.phone}</span>
            </div>
          )}
        </div>
      </div>

      {/* Stats */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Donations"
            value={formatCurrency(stats.total_donations)}
            icon={DollarSign}
          />
          <StatsCard
            title="Donations Count"
            value={stats.donation_count}
            icon={TrendingUp}
          />
          <StatsCard
            title="Unique Donors"
            value={stats.donor_count}
            icon={Users}
          />
          <StatsCard
            title="Active Campaigns"
            value={stats.active_campaigns}
            icon={TrendingUp}
          />
        </div>
      )}

      {/* Campaigns */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Active Campaigns</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {campaigns && campaigns.length > 0 ? (
            campaigns
              .filter((c) => c.is_active)
              .map((campaign) => {
                const percentage = (campaign.current_amount / campaign.goal_amount) * 100;
                return (
                  <div key={campaign.id} className="card p-6">
                    <h3 className="text-xl font-semibold mb-2">{campaign.name}</h3>
                    <p className="text-gray-600 mb-4 line-clamp-2">{campaign.description}</p>
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
                    <Link to={`/campaigns/${campaign.id}`} className="btn-primary w-full text-center">
                      View Campaign
                    </Link>
                  </div>
                );
              })
          ) : (
            <p className="text-gray-500 col-span-full text-center py-8">
              No active campaigns
            </p>
          )}
        </div>
      </div>

      {/* Impact Reports */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Impact Reports</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {impactReports && impactReports.length > 0 ? (
            impactReports.map((report) => (
              <div key={report.id} className="card p-6">
                <h3 className="text-lg font-semibold mb-2">{report.title}</h3>
                <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                  {report.description}
                </p>
                {report.metrics && Object.keys(report.metrics).length > 0 && (
                  <div className="space-y-1 mb-4">
                    {Object.entries(report.metrics)
                      .slice(0, 3)
                      .map(([key, value]) => (
                        <div key={key} className="flex justify-between text-sm">
                          <span className="text-gray-600">{key.replace('_', ' ')}:</span>
                          <span className="font-medium">{value as string}</span>
                        </div>
                      ))}
                  </div>
                )}
                <Link to={`/impact`} className="text-primary-600 hover:underline text-sm">
                  View Details →
                </Link>
              </div>
            ))
          ) : (
            <p className="text-gray-500 col-span-full text-center py-8">
              No impact reports available
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrganizationDetailPage;

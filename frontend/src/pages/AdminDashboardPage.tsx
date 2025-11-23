import { useQuery } from '@tanstack/react-query';
import {
  Users, Building2, TrendingUp, DollarSign, Award,
  AlertCircle, CheckCircle, XCircle
} from 'lucide-react';
import api from '@/services/api';
import { formatCurrency, formatNumber } from '@/utils/formatters';
import StatsCard from '@/components/StatsCard';
import DonationChart from '@/components/DonationChart';

const AdminDashboardPage = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const response = await api.get('/admin/stats');
      return response.data;
    },
  });

  const { data: monthlyData } = useQuery({
    queryKey: ['admin-monthly-donations'],
    queryFn: async () => {
      const response = await api.get('/admin/analytics/donations-by-month');
      return response.data;
    },
  });

  const { data: topDonors} = useQuery({
    queryKey: ['admin-top-donors'],
    queryFn: async () => {
      const response = await api.get('/admin/analytics/top-donors');
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const chartData = monthlyData?.map((item: any) => ({
    name: item.month,
    value: item.total
  })) || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-600 mt-2">Platform overview and analytics</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Users"
          value={formatNumber(stats?.total_users || 0)}
          icon={Users}
          trend={{ value: 12, isPositive: true }}
        />
        <StatsCard
          title="Organizations"
          value={formatNumber(stats?.total_organizations || 0)}
          icon={Building2}
        />
        <StatsCard
          title="Total Donations"
          value={formatCurrency(stats?.total_donations || 0)}
          icon={DollarSign}
          trend={{
            value: stats?.growth_rate || 0,
            isPositive: (stats?.growth_rate || 0) > 0
          }}
        />
        <StatsCard
          title="Active Campaigns"
          value={formatNumber(stats?.active_campaigns || 0)}
          icon={TrendingUp}
        />
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Users</h3>
            <Users className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Total:</span>
              <span className="font-medium">{stats?.total_users}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Active:</span>
              <span className="font-medium text-green-600">{stats?.active_users}</span>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Organizations</h3>
            <Building2 className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Total:</span>
              <span className="font-medium">{stats?.total_organizations}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Verified:</span>
              <span className="font-medium text-blue-600">{stats?.verified_organizations}</span>
            </div>
          </div>
        </div>

        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Donations</h3>
            <TrendingUp className="h-5 w-5 text-gray-400" />
          </div>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Count:</span>
              <span className="font-medium">{stats?.donation_count}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-sm text-gray-600">Average:</span>
              <span className="font-medium">{formatCurrency(stats?.average_donation || 0)}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Donations by Month</h2>
          {chartData.length > 0 ? (
            <DonationChart data={chartData} type="bar" />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>

        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Top Organizations</h2>
          <div className="space-y-3">
            {stats?.top_organizations?.map((org: any, idx: number) => (
              <div key={org.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                <div className="flex items-center space-x-3">
                  <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full font-semibold">
                    {idx + 1}
                  </div>
                  <div>
                    <p className="font-medium">{org.name}</p>
                    <p className="text-sm text-gray-600">{org.donation_count} donations</p>
                  </div>
                </div>
                <span className="font-semibold text-primary-600">
                  {formatCurrency(org.total_donations)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Donors */}
      <div className="card p-6 mb-8">
        <h2 className="text-xl font-semibold mb-4">Top Donors</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Rank
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Name
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Email
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Donations
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  Total Amount
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {topDonors?.map((donor: any, idx: number) => (
                <tr key={donor.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full font-semibold">
                      {idx + 1}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-medium">
                    {donor.name}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-600">
                    {donor.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {donor.donation_count}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap font-semibold text-primary-600">
                    {formatCurrency(donor.total_donated)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="space-y-3">
          {stats?.recent_activity?.slice(0, 5).map((activity: any, idx: number) => (
            <div key={idx} className="flex items-center space-x-4 p-3 bg-gray-50 rounded">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div className="flex-1">
                <p className="text-sm">
                  New donation of <span className="font-medium">{formatCurrency(activity.amount, activity.currency)}</span>
                </p>
                <p className="text-xs text-gray-500">{new Date(activity.date).toLocaleString()}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboardPage;

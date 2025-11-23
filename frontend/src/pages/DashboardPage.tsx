import { useQuery } from '@tanstack/react-query';
import { DollarSign, Heart, TrendingUp, Users } from 'lucide-react';
import { donationsApi } from '@/services/api';
import { formatCurrency, formatDate } from '@/utils/formatters';
import StatsCard from '@/components/StatsCard';
import DonationChart from '@/components/DonationChart';

const DashboardPage = () => {
  const { data: donations, isLoading: donationsLoading } = useQuery({
    queryKey: ['my-donations'],
    queryFn: () => donationsApi.getAll(),
  });

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['my-donation-stats'],
    queryFn: () => donationsApi.getStats(),
  });

  if (donationsLoading || statsLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  // Prepare chart data
  const paymentMethodData = stats?.by_payment_method
    ? Object.entries(stats.by_payment_method).map(([name, value]) => ({
        name: name.replace('_', ' ').toUpperCase(),
        value,
      }))
    : [];

  const statusData = stats?.by_status
    ? Object.entries(stats.by_status).map(([name, value]) => ({
        name: name.toUpperCase(),
        value,
      }))
    : [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Track your donations and view your impact
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Donated"
          value={formatCurrency(stats?.total_amount || 0)}
          icon={DollarSign}
        />
        <StatsCard
          title="Donations Made"
          value={stats?.donation_count || 0}
          icon={Heart}
        />
        <StatsCard
          title="Average Donation"
          value={formatCurrency(stats?.average_donation || 0)}
          icon={TrendingUp}
        />
        <StatsCard
          title="Largest Donation"
          value={formatCurrency(stats?.largest_donation || 0)}
          icon={Users}
        />
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Donations by Payment Method</h2>
          {paymentMethodData.length > 0 ? (
            <DonationChart data={paymentMethodData} type="pie" />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>

        <div className="card p-6">
          <h2 className="text-xl font-semibold mb-4">Donations by Status</h2>
          {statusData.length > 0 ? (
            <DonationChart data={statusData} type="bar" />
          ) : (
            <p className="text-gray-500 text-center py-8">No data available</p>
          )}
        </div>
      </div>

      {/* Recent Donations */}
      <div className="card p-6">
        <h2 className="text-xl font-semibold mb-4">Recent Donations</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Amount
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Payment Method
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Transaction ID
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {donations && donations.length > 0 ? (
                donations.slice(0, 10).map((donation) => (
                  <tr key={donation.id}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatDate(donation.donation_date)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {formatCurrency(donation.amount, donation.currency)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {donation.payment_method?.replace('_', ' ').toUpperCase() || 'N/A'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          donation.status === 'completed'
                            ? 'bg-green-100 text-green-800'
                            : donation.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {donation.status.toUpperCase()}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 font-mono">
                      {donation.transaction_id}
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center text-gray-500">
                    No donations yet
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Calendar, Target, TrendingUp } from 'lucide-react';
import { campaignsApi, organizationsApi, donationsApi } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
import { formatCurrency, formatDate } from '@/utils/formatters';
import { PaymentMethod } from '@/types';

const CampaignDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const campaignId = parseInt(id || '0');
  const { isAuthenticated } = useAuth();
  const queryClient = useQueryClient();

  const [donationAmount, setDonationAmount] = useState('');
  const [paymentMethod, setPaymentMethod] = useState<PaymentMethod>(PaymentMethod.CREDIT_CARD);
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [showDonateForm, setShowDonateForm] = useState(false);

  const { data: campaign, isLoading: campaignLoading } = useQuery({
    queryKey: ['campaign', campaignId],
    queryFn: () => campaignsApi.getById(campaignId),
  });

  const { data: progress } = useQuery({
    queryKey: ['campaign-progress', campaignId],
    queryFn: () => campaignsApi.getProgress(campaignId),
    enabled: !!campaign,
  });

  const { data: organization } = useQuery({
    queryKey: ['organization', campaign?.organization_id],
    queryFn: () => organizationsApi.getById(campaign!.organization_id),
    enabled: !!campaign,
  });

  const { data: donations } = useQuery({
    queryKey: ['campaign-donations', campaignId],
    queryFn: () => donationsApi.getAllPublic({ campaign_id: campaignId }),
  });

  const createDonation = useMutation({
    mutationFn: donationsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['campaign-progress', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['campaign-donations', campaignId] });
      setShowDonateForm(false);
      setDonationAmount('');
      alert('Thank you for your donation!');
    },
  });

  const handleDonate = (e: React.FormEvent) => {
    e.preventDefault();
    if (!campaign) return;

    createDonation.mutate({
      amount: parseFloat(donationAmount),
      currency: campaign.currency,
      payment_method: paymentMethod,
      is_anonymous: isAnonymous,
      organization_id: campaign.organization_id,
      campaign_id: campaign.id,
    });
  };

  if (campaignLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!campaign) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Campaign not found</p>
      </div>
    );
  }

  const percentage = (campaign.current_amount / campaign.goal_amount) * 100;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2">
          <div className="card p-8 mb-8">
            {campaign.image_url && (
              <img
                src={campaign.image_url}
                alt={campaign.name}
                className="w-full h-64 object-cover rounded-lg mb-6"
              />
            )}

            <h1 className="text-3xl font-bold text-gray-900 mb-4">{campaign.name}</h1>

            {organization && (
              <Link
                to={`/organizations/${organization.id}`}
                className="text-primary-600 hover:underline mb-4 inline-block"
              >
                by {organization.name}
              </Link>
            )}

            <div className="prose max-w-none mb-6">
              <p className="text-gray-600">{campaign.description}</p>
            </div>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="flex items-center space-x-2 text-gray-600">
                <Target className="h-5 w-5" />
                <div>
                  <div className="text-sm">Goal</div>
                  <div className="font-semibold">{formatCurrency(campaign.goal_amount)}</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <TrendingUp className="h-5 w-5" />
                <div>
                  <div className="text-sm">Raised</div>
                  <div className="font-semibold">{formatCurrency(campaign.current_amount)}</div>
                </div>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <Calendar className="h-5 w-5" />
                <div>
                  <div className="text-sm">End Date</div>
                  <div className="font-semibold">{formatDate(campaign.end_date)}</div>
                </div>
              </div>
            </div>

            {/* Recent Donations */}
            <div className="mt-8">
              <h2 className="text-2xl font-bold mb-4">Recent Donations</h2>
              <div className="space-y-3">
                {donations && donations.length > 0 ? (
                  donations.slice(0, 5).map((donation) => (
                    <div
                      key={donation.id}
                      className="flex items-center justify-between py-3 border-b"
                    >
                      <div>
                        <span className="font-medium">
                          {donation.is_anonymous ? 'Anonymous' : 'Donor'}
                        </span>
                        <span className="text-sm text-gray-500 ml-2">
                          {formatDate(donation.donation_date)}
                        </span>
                      </div>
                      <span className="font-semibold text-primary-600">
                        {formatCurrency(donation.amount)}
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500">No donations yet. Be the first!</p>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="lg:col-span-1">
          <div className="card p-6 sticky top-8">
            <div className="mb-6">
              <div className="flex justify-between mb-2">
                <span className="text-2xl font-bold text-primary-600">
                  {percentage.toFixed(1)}%
                </span>
                <span className="text-sm text-gray-600">funded</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div
                  className="bg-primary-600 h-3 rounded-full transition-all"
                  style={{ width: `${Math.min(percentage, 100)}%` }}
                />
              </div>
            </div>

            {progress && (
              <div className="space-y-3 mb-6 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Raised</span>
                  <span className="font-semibold">{formatCurrency(progress.current_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Goal</span>
                  <span className="font-semibold">{formatCurrency(progress.goal_amount)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Donors</span>
                  <span className="font-semibold">{progress.donor_count}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Days Remaining</span>
                  <span className="font-semibold">{progress.days_remaining}</span>
                </div>
              </div>
            )}

            {campaign.is_active && (
              <>
                {!showDonateForm ? (
                  <button
                    onClick={() => {
                      if (!isAuthenticated) {
                        alert('Please login to make a donation');
                        return;
                      }
                      setShowDonateForm(true);
                    }}
                    className="btn-primary w-full"
                  >
                    Donate Now
                  </button>
                ) : (
                  <form onSubmit={handleDonate} className="space-y-4">
                    <div>
                      <label className="label">Amount ({campaign.currency})</label>
                      <input
                        type="number"
                        min="1"
                        step="0.01"
                        required
                        className="input"
                        value={donationAmount}
                        onChange={(e) => setDonationAmount(e.target.value)}
                        placeholder="Enter amount"
                      />
                    </div>

                    <div>
                      <label className="label">Payment Method</label>
                      <select
                        className="input"
                        value={paymentMethod}
                        onChange={(e) => setPaymentMethod(e.target.value as PaymentMethod)}
                      >
                        {Object.values(PaymentMethod).map((method) => (
                          <option key={method} value={method}>
                            {method.replace('_', ' ').toUpperCase()}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="flex items-center">
                      <input
                        type="checkbox"
                        id="anonymous"
                        checked={isAnonymous}
                        onChange={(e) => setIsAnonymous(e.target.checked)}
                        className="h-4 w-4 text-primary-600 rounded"
                      />
                      <label htmlFor="anonymous" className="ml-2 text-sm text-gray-700">
                        Make this donation anonymous
                      </label>
                    </div>

                    <div className="flex space-x-2">
                      <button
                        type="submit"
                        disabled={createDonation.isPending}
                        className="btn-primary flex-1"
                      >
                        {createDonation.isPending ? 'Processing...' : 'Complete Donation'}
                      </button>
                      <button
                        type="button"
                        onClick={() => setShowDonateForm(false)}
                        className="btn-secondary"
                      >
                        Cancel
                      </button>
                    </div>
                  </form>
                )}
              </>
            )}

            {!campaign.is_active && (
              <div className="bg-gray-100 p-4 rounded-lg text-center">
                <p className="text-gray-600">This campaign has ended</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CampaignDetailPage;

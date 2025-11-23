import React, { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';

interface Donation {
  id: number;
  amount: number;
  donor_name?: string;
  is_anonymous: boolean;
  campaign?: {
    title: string;
  };
  organization?: {
    name: string;
  };
  created_at: string;
  is_recurring?: boolean;
}

export const LiveDonationFeed: React.FC = () => {
  const [recentDonations, setRecentDonations] = useState<Donation[]>([]);
  const [liveCount, setLiveCount] = useState(0);
  const [isConnected, setIsConnected] = useState(false);

  // Fetch initial donations
  const { data: initialDonations } = useQuery<Donation[]>({
    queryKey: ['recent-donations'],
    queryFn: async () => {
      const response = await api.get('/donations?limit=10&sort=created_at');
      return response.data;
    },
  });

  useEffect(() => {
    if (initialDonations) {
      setRecentDonations(initialDonations);
    }
  }, [initialDonations]);

  // WebSocket connection for live updates
  useEffect(() => {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000';
    const ws = new WebSocket(`${wsUrl}/ws/donations`);

    ws.onopen = () => {
      console.log('Connected to live donation feed');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'donation_created') {
          const newDonation = data.data;

          // Add to recent donations (keep max 10)
          setRecentDonations((prev) => [newDonation, ...prev.slice(0, 9)]);

          // Increment live counter
          setLiveCount((prev) => prev + 1);

          // Show toast notification
          showToast(newDonation);
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log('Disconnected from live donation feed');
      setIsConnected(false);
    };

    // Heartbeat to keep connection alive
    const heartbeat = setInterval(() => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.send('ping');
      }
    }, 30000);

    return () => {
      clearInterval(heartbeat);
      ws.close();
    };
  }, []);

  const showToast = (donation: Donation) => {
    // Create a temporary toast notification
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 animate-slide-in';
    toast.innerHTML = `
      <div class="flex items-center space-x-3">
        <div class="text-2xl">🎉</div>
        <div>
          <p class="font-semibold">New Donation!</p>
          <p class="text-sm">$${donation.amount.toLocaleString()} from ${donation.is_anonymous ? 'Anonymous' : donation.donor_name}</p>
        </div>
      </div>
    `;
    document.body.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 5000);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800 flex items-center space-x-2">
            <span>Live Donations</span>
            <span className="text-2xl">💰</span>
          </h2>
          {liveCount > 0 && (
            <p className="text-sm text-green-600 mt-1">
              {liveCount} new donation{liveCount !== 1 ? 's' : ''} received live!
            </p>
          )}
        </div>
        <div className="flex items-center space-x-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
          <span className="text-sm text-gray-600">
            {isConnected ? 'Live' : 'Disconnected'}
          </span>
        </div>
      </div>

      {/* Donations Feed */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {recentDonations.length > 0 ? (
          recentDonations.map((donation, index) => (
            <div
              key={`${donation.id}-${index}`}
              className={`flex items-center justify-between p-4 rounded-lg transition-all ${
                index < liveCount
                  ? 'bg-green-50 border-2 border-green-200 animate-fade-in'
                  : 'bg-gray-50 hover:bg-gray-100'
              }`}
            >
              <div className="flex items-center space-x-4">
                <div className={`w-12 h-12 rounded-full flex items-center justify-center text-2xl ${
                  donation.is_recurring ? 'bg-purple-100' : 'bg-blue-100'
                }`}>
                  {donation.is_recurring ? '🔄' : '💝'}
                </div>
                <div>
                  <p className="font-semibold text-gray-800">
                    {donation.is_anonymous ? 'Anonymous Donor' : donation.donor_name}
                  </p>
                  <p className="text-sm text-gray-600">
                    {donation.campaign?.title || donation.organization?.name || 'General Donation'}
                  </p>
                  <p className="text-xs text-gray-500">
                    {new Date(donation.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-2xl font-bold text-green-600">
                  ${donation.amount.toLocaleString()}
                </p>
                {donation.is_recurring && (
                  <p className="text-xs text-purple-600 font-semibold">
                    Monthly
                  </p>
                )}
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-8 text-gray-500">
            <div className="text-4xl mb-2">💰</div>
            <p>Waiting for donations...</p>
          </div>
        )}
      </div>

      {/* Stats Bar */}
      {recentDonations.length > 0 && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-blue-600">
                {recentDonations.length}
              </p>
              <p className="text-xs text-gray-600">Recent</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600">
                ${recentDonations.reduce((sum, d) => sum + d.amount, 0).toLocaleString()}
              </p>
              <p className="text-xs text-gray-600">Total</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-purple-600">
                {recentDonations.filter(d => d.is_recurring).length}
              </p>
              <p className="text-xs text-gray-600">Recurring</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

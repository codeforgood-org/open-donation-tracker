import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';

interface Badge {
  id: number;
  badge_type: string;
  description: string;
  earned_at: string;
}

const BADGE_INFO: Record<string, { icon: string; color: string; title: string }> = {
  first_donation: { icon: '🎯', color: 'bg-blue-500', title: 'First Donation' },
  bronze_donor: { icon: '🥉', color: 'bg-orange-600', title: 'Bronze Donor' },
  silver_donor: { icon: '🥈', color: 'bg-gray-400', title: 'Silver Donor' },
  gold_donor: { icon: '🥇', color: 'bg-yellow-400', title: 'Gold Donor' },
  platinum_donor: { icon: '💎', color: 'bg-blue-400', title: 'Platinum Donor' },
  diamond_donor: { icon: '👑', color: 'bg-purple-600', title: 'Diamond Donor' },
  monthly_giver: { icon: '🔄', color: 'bg-green-500', title: 'Monthly Giver' },
  supporter_10: { icon: '⭐', color: 'bg-pink-500', title: 'Supporter x10' },
  supporter_50: { icon: '🌟', color: 'bg-pink-600', title: 'Supporter x50' },
  supporter_100: { icon: '✨', color: 'bg-pink-700', title: 'Supporter x100' },
  campaign_champion: { icon: '🏆', color: 'bg-red-500', title: 'Campaign Champion' },
  early_adopter: { icon: '🚀', color: 'bg-indigo-500', title: 'Early Adopter' },
  generous_heart: { icon: '❤️', color: 'bg-red-400', title: 'Generous Heart' },
  consistent_giver: { icon: '📅', color: 'bg-teal-500', title: 'Consistent Giver' },
  impact_seeker: { icon: '📊', color: 'bg-cyan-500', title: 'Impact Seeker' },
  community_builder: { icon: '🤝', color: 'bg-amber-500', title: 'Community Builder' },
};

export const Badges: React.FC<{ userId?: number }> = ({ userId }) => {
  const { data: badges, isLoading, error } = useQuery<Badge[]>({
    queryKey: ['badges', userId],
    queryFn: async () => {
      const url = userId ? `/gamification/users/${userId}/badges` : '/gamification/my-badges';
      const response = await api.get(url);
      return response.data;
    },
  });

  const { data: achievements } = useQuery({
    queryKey: ['achievements', userId],
    queryFn: async () => {
      const url = userId ? `/gamification/users/${userId}/achievements` : '/gamification/my-achievements';
      const response = await api.get(url);
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(8)].map((_, i) => (
          <div key={i} className="h-32 bg-gray-200 rounded-lg animate-pulse"></div>
        ))}
      </div>
    );
  }

  if (error) {
    return <div className="text-red-500">Failed to load badges</div>;
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">
          Badges & Achievements
        </h2>
        {achievements && (
          <div className="text-sm text-gray-600">
            {badges?.length || 0} / {Object.keys(BADGE_INFO).length} collected
          </div>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {badges?.map((badge) => {
          const info = BADGE_INFO[badge.badge_type] || {
            icon: '🎖️',
            color: 'bg-gray-500',
            title: badge.badge_type,
          };

          return (
            <div
              key={badge.id}
              className="bg-white rounded-lg shadow-md p-4 flex flex-col items-center text-center hover:shadow-lg transition-shadow"
            >
              <div
                className={`w-16 h-16 rounded-full ${info.color} flex items-center justify-center text-3xl mb-3`}
              >
                {info.icon}
              </div>
              <h3 className="font-semibold text-gray-800 mb-1">{info.title}</h3>
              <p className="text-xs text-gray-600 mb-2">{badge.description}</p>
              <p className="text-xs text-gray-400">
                {new Date(badge.earned_at).toLocaleDateString()}
              </p>
            </div>
          );
        })}

        {/* Show locked badges */}
        {Object.entries(BADGE_INFO)
          .filter(([type]) => !badges?.some((b) => b.badge_type === type))
          .map(([type, info]) => (
            <div
              key={type}
              className="bg-gray-100 rounded-lg shadow-md p-4 flex flex-col items-center text-center opacity-50"
            >
              <div className="w-16 h-16 rounded-full bg-gray-300 flex items-center justify-center text-3xl mb-3 grayscale">
                🔒
              </div>
              <h3 className="font-semibold text-gray-500 mb-1">{info.title}</h3>
              <p className="text-xs text-gray-400">Not yet unlocked</p>
            </div>
          ))}
      </div>

      {achievements && (
        <div className="mt-8 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">
            Your Progress
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white rounded-lg p-4">
              <div className="text-3xl font-bold text-green-600">
                ${achievements.total_donated?.toLocaleString() || 0}
              </div>
              <div className="text-sm text-gray-600">Total Donated</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="text-3xl font-bold text-blue-600">
                {achievements.donation_count || 0}
              </div>
              <div className="text-sm text-gray-600">Donations Made</div>
            </div>
            <div className="bg-white rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-3xl font-bold text-purple-600">
                    {achievements.level || 'Bronze'}
                  </div>
                  <div className="text-sm text-gray-600">Current Level</div>
                </div>
                <div className="text-4xl">
                  {BADGE_INFO[`${achievements.level?.toLowerCase()}_donor`]?.icon || '🥉'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

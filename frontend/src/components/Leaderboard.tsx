import React from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../lib/api';

interface LeaderboardEntry {
  id: number;
  user_id: number;
  level: string;
  total_donated: number;
  donation_count: number;
  points: number;
  rank: number;
  user?: {
    full_name: string;
    avatar_url?: string;
  };
}

const LEVEL_COLORS: Record<string, string> = {
  Bronze: 'bg-orange-600',
  Silver: 'bg-gray-400',
  Gold: 'bg-yellow-400',
  Platinum: 'bg-blue-400',
  Diamond: 'bg-purple-600',
};

const LEVEL_ICONS: Record<string, string> = {
  Bronze: '🥉',
  Silver: '🥈',
  Gold: '🥇',
  Platinum: '💎',
  Diamond: '👑',
};

export const Leaderboard: React.FC<{ limit?: number }> = ({ limit = 10 }) => {
  const { data: leaderboard, isLoading, error } = useQuery<LeaderboardEntry[]>({
    queryKey: ['leaderboard', limit],
    queryFn: async () => {
      const response = await api.get(`/gamification/leaderboard?limit=${limit}`);
      return response.data;
    },
  });

  if (isLoading) {
    return (
      <div className="animate-pulse">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-200 rounded mb-2"></div>
        ))}
      </div>
    );
  }

  if (error) {
    return <div className="text-red-500">Failed to load leaderboard</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        🏆 Top Donors Leaderboard
      </h2>
      <div className="space-y-3">
        {leaderboard?.map((entry, index) => (
          <div
            key={entry.id}
            className={`flex items-center justify-between p-4 rounded-lg transition-all hover:shadow-md ${
              index < 3 ? 'bg-gradient-to-r from-yellow-50 to-orange-50' : 'bg-gray-50'
            }`}
          >
            <div className="flex items-center space-x-4">
              <div
                className={`w-12 h-12 rounded-full flex items-center justify-center text-white font-bold text-lg ${
                  index === 0
                    ? 'bg-yellow-500'
                    : index === 1
                    ? 'bg-gray-400'
                    : index === 2
                    ? 'bg-orange-600'
                    : 'bg-gray-300'
                }`}
              >
                {index < 3 ? ['🥇', '🥈', '🥉'][index] : entry.rank}
              </div>

              {entry.user?.avatar_url ? (
                <img
                  src={entry.user.avatar_url}
                  alt={entry.user.full_name}
                  className="w-12 h-12 rounded-full object-cover"
                />
              ) : (
                <div className="w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold">
                  {entry.user?.full_name?.charAt(0) || '?'}
                </div>
              )}

              <div>
                <div className="font-semibold text-gray-800">
                  {entry.user?.full_name || 'Anonymous'}
                </div>
                <div className="flex items-center space-x-2">
                  <span className={`px-2 py-1 rounded text-xs font-semibold text-white ${LEVEL_COLORS[entry.level]}`}>
                    {LEVEL_ICONS[entry.level]} {entry.level}
                  </span>
                  <span className="text-xs text-gray-500">
                    {entry.donation_count} donations
                  </span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-green-600">
                ${entry.total_donated.toLocaleString()}
              </div>
              <div className="text-sm text-gray-500">
                {entry.points.toLocaleString()} pts
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

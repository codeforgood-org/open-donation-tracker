import React from 'react';
import { Leaderboard } from '../components/Leaderboard';
import { Badges } from '../components/Badges';
import { SocialFeed } from '../components/SocialFeed';
import { LiveDonationFeed } from '../components/LiveDonationFeed';

const LeaderboardPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-12">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-4">
            Community Leaderboard
          </h1>
          <p className="text-xl opacity-90">
            Celebrating our amazing donors and their impact
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Leaderboard */}
          <div className="lg:col-span-2 space-y-8">
            <Leaderboard limit={20} />

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">
                My Achievements
              </h2>
              <Badges />
            </div>
          </div>

          {/* Right Column - Live Feed & Activity */}
          <div className="space-y-8">
            <LiveDonationFeed />
            <SocialFeed />
          </div>
        </div>

        {/* Additional Stats Section */}
        <div className="mt-12 bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            Platform Impact
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
              <div className="text-4xl mb-2">💰</div>
              <div className="text-3xl font-bold text-green-600 mb-1">
                $2.5M+
              </div>
              <div className="text-sm text-gray-600">Total Raised</div>
            </div>
            <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg">
              <div className="text-4xl mb-2">👥</div>
              <div className="text-3xl font-bold text-blue-600 mb-1">
                10,000+
              </div>
              <div className="text-sm text-gray-600">Active Donors</div>
            </div>
            <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
              <div className="text-4xl mb-2">🎯</div>
              <div className="text-3xl font-bold text-purple-600 mb-1">
                500+
              </div>
              <div className="text-sm text-gray-600">Campaigns Funded</div>
            </div>
            <div className="text-center p-6 bg-gradient-to-br from-orange-50 to-orange-100 rounded-lg">
              <div className="text-4xl mb-2">🏆</div>
              <div className="text-3xl font-bold text-orange-600 mb-1">
                50,000+
              </div>
              <div className="text-sm text-gray-600">Badges Earned</div>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">
            How the Leaderboard Works
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg p-6">
              <div className="text-3xl mb-3">⭐</div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Earn Points
              </h3>
              <p className="text-gray-600 text-sm">
                Every dollar donated earns you 1 point. Bonus points for multiple donations!
              </p>
            </div>
            <div className="bg-white rounded-lg p-6">
              <div className="text-3xl mb-3">🏅</div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Level Up
              </h3>
              <p className="text-gray-600 text-sm">
                Progress through Bronze, Silver, Gold, Platinum, and Diamond levels.
              </p>
            </div>
            <div className="bg-white rounded-lg p-6">
              <div className="text-3xl mb-3">🎖️</div>
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                Unlock Badges
              </h3>
              <p className="text-gray-600 text-sm">
                Complete achievements to earn exclusive badges and recognition.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LeaderboardPage;

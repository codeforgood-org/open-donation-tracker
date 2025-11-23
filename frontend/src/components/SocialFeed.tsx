import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import api from '../lib/api';

interface Comment {
  id: number;
  user_id: number;
  content: string;
  parent_id?: number;
  created_at: string;
  user?: {
    full_name: string;
    avatar_url?: string;
  };
  replies?: Comment[];
}

interface ActivityItem {
  id: number;
  user_id: number;
  activity_type: string;
  description: string;
  created_at: string;
  user?: {
    full_name: string;
    avatar_url?: string;
  };
}

const ACTIVITY_ICONS: Record<string, string> = {
  donation: '💰',
  campaign_created: '🎯',
  badge_earned: '🏆',
  comment: '💬',
  review: '⭐',
  share: '📤',
  level_up: '⬆️',
};

export const SocialFeed: React.FC<{ campaignId?: number }> = ({ campaignId }) => {
  const [commentText, setCommentText] = useState('');
  const [replyTo, setReplyTo] = useState<number | null>(null);
  const queryClient = useQueryClient();

  // Fetch activity feed
  const { data: activities, isLoading: activitiesLoading } = useQuery<ActivityItem[]>({
    queryKey: ['activity-feed'],
    queryFn: async () => {
      const response = await api.get('/social/activity-feed?limit=20');
      return response.data;
    },
  });

  // Fetch comments for campaign
  const { data: comments, isLoading: commentsLoading } = useQuery<Comment[]>({
    queryKey: ['comments', campaignId],
    queryFn: async () => {
      if (!campaignId) return [];
      const response = await api.get(`/social/campaigns/${campaignId}/comments`);
      return response.data;
    },
    enabled: !!campaignId,
  });

  // Create comment mutation
  const createCommentMutation = useMutation({
    mutationFn: async (data: { content: string; campaign_id?: number; parent_id?: number }) => {
      await api.post('/social/comments', data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['comments'] });
      setCommentText('');
      setReplyTo(null);
    },
  });

  const handleSubmitComment = (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentText.trim()) return;

    createCommentMutation.mutate({
      content: commentText,
      campaign_id: campaignId,
      parent_id: replyTo || undefined,
    });
  };

  const renderComment = (comment: Comment, depth: number = 0) => (
    <div key={comment.id} className={`${depth > 0 ? 'ml-8 mt-2' : 'mt-4'}`}>
      <div className="bg-white rounded-lg p-4 shadow-sm">
        <div className="flex items-start space-x-3">
          {comment.user?.avatar_url ? (
            <img
              src={comment.user.avatar_url}
              alt={comment.user.full_name}
              className="w-10 h-10 rounded-full object-cover"
            />
          ) : (
            <div className="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white font-semibold">
              {comment.user?.full_name?.charAt(0) || '?'}
            </div>
          )}
          <div className="flex-1">
            <div className="flex items-center space-x-2">
              <span className="font-semibold text-gray-800">
                {comment.user?.full_name || 'Anonymous'}
              </span>
              <span className="text-xs text-gray-500">
                {new Date(comment.created_at).toLocaleString()}
              </span>
            </div>
            <p className="text-gray-700 mt-2">{comment.content}</p>
            <button
              onClick={() => setReplyTo(comment.id)}
              className="text-sm text-blue-600 hover:text-blue-700 mt-2"
            >
              Reply
            </button>
          </div>
        </div>
      </div>
      {comment.replies?.map((reply) => renderComment(reply, depth + 1))}
    </div>
  );

  if (campaignId) {
    // Campaign-specific comments view
    return (
      <div className="bg-gray-50 rounded-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">
          Comments ({comments?.length || 0})
        </h3>

        {/* Comment Form */}
        <form onSubmit={handleSubmitComment} className="mb-6">
          {replyTo && (
            <div className="mb-2 flex items-center justify-between bg-blue-50 p-2 rounded">
              <span className="text-sm text-blue-700">Replying to comment</span>
              <button
                type="button"
                onClick={() => setReplyTo(null)}
                className="text-blue-700 hover:text-blue-900"
              >
                ✕
              </button>
            </div>
          )}
          <textarea
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Write a comment..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            rows={3}
          />
          <button
            type="submit"
            disabled={!commentText.trim() || createCommentMutation.isPending}
            className="mt-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {createCommentMutation.isPending ? 'Posting...' : 'Post Comment'}
          </button>
        </form>

        {/* Comments List */}
        {commentsLoading ? (
          <div className="text-center py-8">Loading comments...</div>
        ) : comments && comments.length > 0 ? (
          <div className="space-y-2">
            {comments.map((comment) => renderComment(comment))}
          </div>
        ) : (
          <div className="text-center py-8 text-gray-500">
            No comments yet. Be the first to comment!
          </div>
        )}
      </div>
    );
  }

  // Global activity feed view
  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Recent Activity
      </h2>

      {activitiesLoading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-lg animate-pulse"></div>
          ))}
        </div>
      ) : activities && activities.length > 0 ? (
        <div className="space-y-4">
          {activities.map((activity) => (
            <div
              key={activity.id}
              className="flex items-start space-x-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="text-2xl">
                {ACTIVITY_ICONS[activity.activity_type] || '📋'}
              </div>
              <div className="flex-1">
                <div className="flex items-center space-x-2">
                  {activity.user?.avatar_url ? (
                    <img
                      src={activity.user.avatar_url}
                      alt={activity.user.full_name}
                      className="w-8 h-8 rounded-full object-cover"
                    />
                  ) : (
                    <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-semibold">
                      {activity.user?.full_name?.charAt(0) || '?'}
                    </div>
                  )}
                  <span className="font-semibold text-gray-800">
                    {activity.user?.full_name || 'Someone'}
                  </span>
                </div>
                <p className="text-gray-700 mt-1">{activity.description}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(activity.created_at).toLocaleString()}
                </p>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">🌟</div>
          <p className="text-gray-500">No recent activity</p>
        </div>
      )}
    </div>
  );
};

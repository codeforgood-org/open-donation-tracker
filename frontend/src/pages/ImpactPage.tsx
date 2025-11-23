import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { TrendingUp, FileText } from 'lucide-react';
import { impactReportsApi } from '@/services/api';
import { formatDate } from '@/utils/formatters';

const ImpactPage = () => {
  const { data: reports, isLoading } = useQuery({
    queryKey: ['impact-reports'],
    queryFn: () => impactReportsApi.getAll(),
  });

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Impact Reports</h1>
        <p className="text-gray-600 mt-2">
          See the real-world impact of donations across all organizations
        </p>
      </div>

      {/* Hero Stats */}
      <div className="card p-8 mb-8 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
        <div className="text-center">
          <TrendingUp className="h-12 w-12 mx-auto mb-4" />
          <h2 className="text-3xl font-bold mb-2">Tracking Real Impact</h2>
          <p className="text-primary-100 max-w-2xl mx-auto">
            Transparency is at the heart of what we do. Every organization provides detailed
            impact reports showing exactly how donations are being used and the difference
            they're making.
          </p>
        </div>
      </div>

      {/* Impact Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports && reports.length > 0 ? (
          reports.map((report) => (
            <div key={report.id} className="card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <FileText className="h-8 w-8 text-primary-600" />
                <span className="text-xs text-gray-500">
                  {formatDate(report.period_start)} - {formatDate(report.period_end)}
                </span>
              </div>

              <h3 className="text-xl font-semibold text-gray-900 mb-2">{report.title}</h3>

              <p className="text-gray-600 mb-4 line-clamp-3">{report.description}</p>

              {/* Metrics */}
              {report.metrics && Object.keys(report.metrics).length > 0 && (
                <div className="mb-4 space-y-2">
                  <h4 className="text-sm font-semibold text-gray-700">Impact Metrics:</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(report.metrics)
                      .slice(0, 4)
                      .map(([key, value]) => (
                        <div key={key} className="bg-gray-50 p-2 rounded">
                          <div className="text-xs text-gray-600 capitalize">
                            {key.replace(/_/g, ' ')}
                          </div>
                          <div className="text-lg font-bold text-primary-600">
                            {typeof value === 'number' ? value.toLocaleString() : value}
                          </div>
                        </div>
                      ))}
                  </div>
                </div>
              )}

              {/* Images */}
              {report.images && report.images.length > 0 && (
                <div className="mb-4">
                  <div className="grid grid-cols-3 gap-2">
                    {report.images.slice(0, 3).map((image, idx) => (
                      <img
                        key={idx}
                        src={image}
                        alt={`Impact ${idx + 1}`}
                        className="w-full h-20 object-cover rounded"
                      />
                    ))}
                  </div>
                </div>
              )}

              <Link
                to={`/organizations/${report.organization_id}`}
                className="text-primary-600 hover:underline text-sm font-medium"
              >
                View Organization →
              </Link>

              {report.report_url && (
                <a
                  href={report.report_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ml-4 text-primary-600 hover:underline text-sm font-medium"
                >
                  Full Report ↗
                </a>
              )}
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <FileText className="h-16 w-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500 mb-4">No impact reports available yet</p>
            <p className="text-sm text-gray-400">
              Check back soon to see how organizations are making a difference
            </p>
          </div>
        )}
      </div>

      {/* Info Section */}
      <div className="mt-12 card p-8 bg-gray-50">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Understanding Impact Reports</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">What are Impact Reports?</h3>
            <p className="text-sm text-gray-600">
              Impact reports detail how organizations use donations and the measurable outcomes
              they achieve, providing full transparency to donors.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Key Metrics</h3>
            <p className="text-sm text-gray-600">
              Organizations report specific metrics like people helped, services provided, or
              environmental impact, depending on their mission.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 mb-2">Transparency Score</h3>
            <p className="text-sm text-gray-600">
              Each organization receives a transparency score based on their reporting frequency,
              detail, and accountability measures.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ImpactPage;

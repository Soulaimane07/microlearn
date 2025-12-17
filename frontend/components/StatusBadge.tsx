import React from 'react';
import { CheckCircle2, XCircle, Loader2, Clock } from 'lucide-react';

interface StatusBadgeProps {
  status: 'success' | 'failed' | 'in-progress' | 'pending';
  label?: string;
}

export function StatusBadge({ status, label }: StatusBadgeProps) {
  const configs = {
    success: {
      icon: CheckCircle2,
      bg: 'bg-green-100',
      text: 'text-green-700',
      iconColor: 'text-green-600',
      label: label || 'Success',
    },
    failed: {
      icon: XCircle,
      bg: 'bg-red-100',
      text: 'text-red-700',
      iconColor: 'text-red-600',
      label: label || 'Failed',
    },
    'in-progress': {
      icon: Loader2,
      bg: 'bg-blue-100',
      text: 'text-blue-700',
      iconColor: 'text-blue-600',
      label: label || 'In Progress',
    },
    pending: {
      icon: Clock,
      bg: 'bg-gray-100',
      text: 'text-gray-700',
      iconColor: 'text-gray-600',
      label: label || 'Pending',
    },
  };

  const config = configs[status];
  const Icon = config.icon;

  return (
    <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full ${config.bg}`}>
      <Icon className={`w-3.5 h-3.5 ${config.iconColor} ${status === 'in-progress' ? 'animate-spin' : ''}`} />
      <span className={`text-xs ${config.text}`}>{config.label}</span>
    </div>
  );
}

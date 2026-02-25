export interface TimerState {
  id: string;
  duration_seconds: number;
  elapsed_seconds: number;
  is_running: boolean;
  urgency_level: UrgencyLevel;
  created_at: string;
  last_reset_at: string;
}

export interface TimerResponse {
  timer: TimerState;
}

export type UrgencyLevel = 'safe' | 'caution' | 'urgent' | 'critical';

export interface CreateTimerRequest {
  duration_seconds: number;
}

export interface StartTimerRequest {
  timer_id: string;
}

export interface StopTimerRequest {
  timer_id: string;
}

export interface ResetTimerRequest {
  timer_id: string;
}

export interface ErrorResponse {
  detail: string;
}

export const getUrgencyLevel = (remainingSeconds: number, durationSeconds: number): UrgencyLevel => {
  const percentRemaining = (remainingSeconds / durationSeconds) * 100;

  if (percentRemaining > 50) return 'safe';
  if (percentRemaining > 25) return 'caution';
  if (percentRemaining > 10) return 'urgent';
  return 'critical';
};

export const getUrgencyColor = (urgencyLevel: UrgencyLevel): string => {
  const colors: Record<UrgencyLevel, string> = {
    safe: '#00FF00',
    caution: '#FFFF00',
    urgent: '#FF8800',
    critical: '#FF0000',
  };
  return colors[urgencyLevel];
};

export const getTimeRemaining = (state: TimerState): number => {
  return Math.max(0, state.duration_seconds - state.elapsed_seconds);
};

export const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
};

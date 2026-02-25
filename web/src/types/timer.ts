export type TimerStatus = 'running' | 'paused' | 'expired';

export type UrgencyLevel = 'low' | 'medium' | 'high' | 'critical';

export interface ColourIntensity {
  red: number;
  green: number;
  blue: number;
}

export interface FacialExpression {
  eyes: string;
  mouth: string;
  intensity: number;
}

export interface Timer {
  id: string;
  initialDuration: number;
  remainingTime: number;
  status: TimerStatus;
  createdAt: string;
  startedAt: string | null;
}

export interface TimerCreateRequest {
  duration: number;
}

export interface TimerState {
  id: string;
  remainingTime: number;
  remainingPercentage: number;
  urgencyLevel: UrgencyLevel;
  colourIntensity: ColourIntensity;
  facialExpression: FacialExpression;
}

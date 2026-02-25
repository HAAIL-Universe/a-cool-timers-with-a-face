import type {
  Timer,
  TimerStatus,
  UrgencyLevel,
  FacialExpression,
  ColourIntensity,
  TimerState,
} from '../types/timer';

export const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const TIMERS_ENDPOINT = `${BASE_URL}/timers`;

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error: ${response.status} ${error}`);
  }
  return response.json() as Promise<T>;
}

export async function createTimer(duration: number): Promise<Timer> {
  const response = await fetch(TIMERS_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ duration }),
  });
  return handleResponse<Timer>(response);
}

export async function listTimers(): Promise<Timer[]> {
  const response = await fetch(TIMERS_ENDPOINT, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<Timer[]>(response);
}

export async function getTimer(timerId: string): Promise<Timer> {
  const response = await fetch(`${TIMERS_ENDPOINT}/${timerId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<Timer>(response);
}

export async function deleteTimer(timerId: string): Promise<void> {
  const response = await fetch(`${TIMERS_ENDPOINT}/${timerId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`API error: ${response.status} ${error}`);
  }
}

export async function resetTimer(timerId: string): Promise<Timer> {
  const response = await fetch(`${TIMERS_ENDPOINT}/${timerId}/reset`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<Timer>(response);
}

export async function getTimerState(timerId: string): Promise<TimerState> {
  const response = await fetch(`${TIMERS_ENDPOINT}/${timerId}/state`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return handleResponse<TimerState>(response);
}

export async function startTimer(duration: number): Promise<Timer> {
  const timer = await createTimer(duration);
  return timer;
}

export async function stopTimer(): Promise<TimerState> {
  const timers = await listTimers();
  if (timers.length === 0) {
    throw new Error('No active timer found');
  }
  const activeTimer = timers.find((t) => t.status === 'running');
  if (!activeTimer) {
    throw new Error('No active timer found');
  }
  return getTimerState(activeTimer.id);
}

export async function getUrgency(timerId: string): Promise<UrgencyLevel> {
  const state = await getTimerState(timerId);
  return state.urgencyLevel;
}

export async function getStatus(timerId: string): Promise<TimerStatus> {
  const timer = await getTimer(timerId);
  return timer.status;
}

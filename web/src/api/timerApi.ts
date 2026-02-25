import { Timer, TimerState } from '../types/timer';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function request<T>(
  method: string,
  path: string,
  body?: Record<string, unknown>
): Promise<T> {
  const options: RequestInit = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) {
    throw new Error(`API error: ${res.status}`);
  }
  return res.json();
}

export async function createTimer(duration: number): Promise<Timer> {
  return request<Timer>('POST', '/timers', { initial_seconds: duration });
}

export async function getTimerState(timerId: string): Promise<TimerState> {
  return request<TimerState>('GET', `/timers/${timerId}/state`);
}

export async function startTimer(timerId: string): Promise<TimerState> {
  return request<TimerState>('POST', `/timers/${timerId}/start`);
}

export async function pauseTimer(timerId: string): Promise<TimerState> {
  return request<TimerState>('POST', `/timers/${timerId}/pause`);
}

export async function resetTimer(timerId: string): Promise<TimerState> {
  return request<TimerState>('POST', `/timers/${timerId}/reset`);
}

export async function deleteTimer(timerId: string): Promise<void> {
  await request<void>('DELETE', `/timers/${timerId}`);
}

export { BASE_URL };

import axios, { AxiosInstance } from 'axios';
import {
  TimerState,
  UrgencyState,
  TimerConfigRequest,
  TimerResponse,
  UrgencyResponse,
} from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const client: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function getTimerState(): Promise<TimerState> {
  const response = await client.get<TimerResponse>('/timer');
  return response.data as TimerState;
}

export async function configureTimer(duration: number): Promise<TimerState> {
  const body: TimerConfigRequest = { duration };
  const response = await client.post<TimerResponse>('/timer', body);
  return response.data as TimerState;
}

export async function resetTimer(): Promise<TimerState> {
  const response = await client.post<TimerResponse>('/timer/reset');
  return response.data as TimerState;
}

export async function pauseTimer(): Promise<TimerState> {
  const response = await client.post<TimerResponse>('/timer/pause');
  return response.data as TimerState;
}

export async function resumeTimer(): Promise<TimerState> {
  const response = await client.post<TimerResponse>('/timer/resume');
  return response.data as TimerState;
}

export async function getUrgency(): Promise<UrgencyState> {
  const response = await client.get<UrgencyResponse>('/urgency');
  return response.data as UrgencyState;
}

export default client;

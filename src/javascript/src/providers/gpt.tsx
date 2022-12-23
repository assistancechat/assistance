import {
  createContext,
} from '@builder.io/qwik';

export interface GptState {
  accessToken: string
  agentName: string
  promptTemplate: string
  initialPrompt: string
  messages: string[]
}

export const GptContext = createContext<GptState>('gpt-state');

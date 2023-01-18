import {
  createContext,
} from '@builder.io/qwik';

type Message = {
  message: string
}

export interface GptState {
  accessToken: string
  agentName: string
  promptTemplate: string
  initialPrompt: string
  conversation: Message[]
}

export const GptContext = createContext<GptState>('gpt-state');

import {
  createContext,
} from '@builder.io/qwik';

export interface PromptState {
  agentName: string
  template: string
  formContents: Record<string, string>
}

export const FormContext = createContext<Record<string, string>>('form-state');
export const PromptContext = createContext<PromptState>('prompt-state');

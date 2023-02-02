import {
  createContext,
} from '@builder.io/qwik';

export type FormUpdateCounterState = {
  counter: number
}

export const FormRecordIdContext = createContext<Record<string, string>>('form-record-id-state');
export const FormPromptIdContext = createContext<Record<string, string>>('form-prompt-id-state');

// This is a work-a-round as records don't appear to recursively trigger Qwik
// useTasks
export const FormUpdateCounterContext = createContext<FormUpdateCounterState>('form-update-counter');

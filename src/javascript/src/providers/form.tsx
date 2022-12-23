import {
  createContext,
} from '@builder.io/qwik';

export const FormRecordIdContext = createContext<Record<string, string>>('form-record-id-state');
export const FormPromptIdContext = createContext<Record<string, string>>('form-prompt-id-state');

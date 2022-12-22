import {
  createContext,
} from '@builder.io/qwik';


export const FormContext = createContext<Record<string, string>>('form-content');

import { component$, useContext } from '@builder.io/qwik';
import { RegisteredComponent } from "@builder.io/sdk-qwik";
import { FormContext } from "~/providers/form";

type Item = {
  recordId: string
  formText: string
}



const Form = component$((props: {hasButton: boolean, buttonText: string, items: Item[]}) => {
  const formState = useContext(FormContext);

  if (props.items === undefined || props.items.length === 0) {
    return <></>
  }
  return (
    <div class="container mx-auto items-center">
      <div class="px-5 py-5 flex justify-between bg-white border-b-2 shadow-lg rounded-lg">
        <form class="w-full">
          {props.items.map(({recordId, formText}) => (
            <div class="flex flex-wrap -mx-3 mb-6">
              <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
                  {formText}
                </label>
                <input
                  id={recordId}
                  value={formState[recordId]}
                  onChange$={(event) => {formState[recordId] = event.target.value}}
                  type="text"
                  class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500"
                />
              </div>
            </div>
          ))}
          <button style={{display: `${props.hasButton ? "block" : "none"}`}} class="btn btn-primary sm:mb-0" type="button">
            {props.buttonText}
          </button>
        </form>
      </div>
    </div>
  );
});


export const FormItem: RegisteredComponent = {
  component: Form,
  name: 'Form',
  builtIn: true,
  inputs: [
    {
      name: 'hasButton',
      type: "boolean"
    },
    {
      name: 'buttonText',
      type: "text"
    },
    {
      name: 'items',
      type: 'list',
      subFields: [
        {
          name: "recordId",
          type: 'string',
        },
        {
          name: "formText",
          type: 'string'
        }
      ]
    }
  ],
}
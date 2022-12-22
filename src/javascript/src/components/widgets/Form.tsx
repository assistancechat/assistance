import { component$ } from "@builder.io/qwik";
import { RegisteredComponent } from "@builder.io/sdk-qwik";

type Item = {
  recordId: string
  promptText: string
  interfaceText: string
}

const Form = component$((props: {items: Item[]}) => {
  if (props.items === undefined || props.items.length === 0) {
    return <></>
  }
  return (
    <div class="container mx-auto items-center">
      <div class="px-5 py-5 flex justify-between bg-white border-b-2 shadow-lg rounded-lg ">
        <form class="w-full">
          {props.items.map(({recordId, promptText, interfaceText}) => (
            <div class="flex flex-wrap -mx-3 mb-6">
              <div class="w-full px-3">
                <label class="block uppercase tracking-wide text-gray-700 text-xs font-bold mb-2" for="grid-password">
                  {interfaceText}
                </label>
                <input class="appearance-none block w-full bg-gray-200 text-gray-700 border border-gray-200 rounded py-3 px-4 mb-3 leading-tight focus:outline-none focus:bg-white focus:border-gray-500" id="nick" type="text"/>
              </div>
            </div>
          ))}
          <div class="md:flex md:items-center">
            <div>
              <button class="btn btn-primary sm:mb-0 w-full" type="button">
                Send chat URL to your email inbox
              </button>
            </div>
          </div>
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
      name: 'items',
      type: 'list',
      subFields: [
        {
          name: "recordId",
          type: 'string',
        },
        {
          name: "promptText",
          type: 'string'
        },
        {
          name: "interfaceText",
          type: 'string'
        }
      ]
    }
  ],
}
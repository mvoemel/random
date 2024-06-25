import { forwardRef, useImperativeHandle, useState } from "react";
import { delay } from "./utils";
import Stack from "./Stack";
import {
  CheckCircledIcon,
  ExclamationTriangleIcon,
} from "@radix-ui/react-icons";

interface Props {
  enableStartButton: () => void;
}

export type RPNUPN_Ref = {
  runAnimation: (input: string, stepMode?: boolean) => void;
};

const ReversePolishNotationPushdownAutomaton = forwardRef<RPNUPN_Ref, Props>(
  (props, ref) => {
    const { enableStartButton } = props;

    useImperativeHandle(ref, () => ({
      runAnimation: (input, stepMode) => {
        calculate(input, !!stepMode);
      },
    }));

    const DELAY_IN_MS = 2000;
    const VALID_OPERATORS = ["+", "*"];

    const [displayStack, setDisplayStack] = useState<number[]>([]);
    const [displayRemainingInput, setDisplayRemainingInput] =
      useState<string>("");
    const [displayCalculationSteps, setDisplayCalculationSteps] =
      useState<string>("");

    const [error, setError] = useState<string>("");
    const [result, setResult] = useState<string>("");

    const calculate: (input: string, stepMode: boolean) => void = async (
      input,
      stepMode
    ) => {
      setDisplayStack([]);
      setDisplayRemainingInput("");
      setDisplayCalculationSteps("");
      setResult("");
      setError("");

      const stack = new Stack();
      let remainingInput = input;
      let calculationSteps = `(${remainingInput}, ${stack.get()})`;

      if (remainingInput.toString() === "") {
        setError("Empty string was given");
        enableStartButton();
        return;
      }

      if (stepMode) {
        setDisplayStack(stack.get());
        setDisplayRemainingInput(remainingInput);
        setDisplayCalculationSteps(calculationSteps);
        await delay(DELAY_IN_MS);
      }

      while (remainingInput.length > 0) {
        calculationSteps = calculationSteps + " |- ";

        const currentSymbol = remainingInput[0];
        const isDigit = !isNaN(parseFloat(currentSymbol));
        const isOperator = VALID_OPERATORS.includes(currentSymbol);

        if (isDigit) {
          stack.push(parseInt(currentSymbol));
        } else if (isOperator) {
          // Stack has at least two elements
          if (stack.size() > 1) {
            const numberOne = stack.pop() ?? 0;
            const numberTwo = stack.pop() ?? 0;

            switch (currentSymbol) {
              case "+":
                stack.push(numberOne + numberTwo);
                break;
              case "-":
                stack.push(numberOne - numberTwo);
                break;
              case "*":
                stack.push(numberOne * numberTwo);
                break;
              case "/":
                stack.push(numberOne / numberTwo);
            }
          } else {
            setError("Operator needs to have two Numbers as predecessors");
            enableStartButton();
            return;
          }
        } else {
          setError("Invalid Operator");
          enableStartButton();
          return;
        }
        remainingInput = remainingInput.slice(1);

        if (stepMode) {
          setDisplayStack(stack.get());
          setDisplayRemainingInput(remainingInput);
          calculationSteps =
            calculationSteps + `(${remainingInput}, ${stack.get()})`;
          setDisplayCalculationSteps(calculationSteps);
          await delay(DELAY_IN_MS);
        }
      } // end while-loop

      if (stack.size() > 1) {
        setError("Too few Operators were given");
        enableStartButton();
        return;
      }

      setResult(stack.get()[0] + "");
      enableStartButton();
    };

    return (
      <>
        <div className="mb-5 flex flex-row items-center justify-center">
          <h2 className="mx-5">
            <b className="text-yellow-300">{displayRemainingInput.charAt(0)}</b>
            {displayRemainingInput.slice(1)}
          </h2>
          <div className="flex flex-col items-center">
            {[...displayStack].reverse().map((item, index) => (
              <div
                key={index}
                className="w-[100px] border border-white text-center"
              >
                {item}
              </div>
            ))}
          </div>
        </div>
        <div className="mb-5">{displayCalculationSteps}</div>
        {result && (
          <div className="bg-emerald-500/15 p-3 rounded-md flex items-center gap-x-2 text-sm text-emerald-500">
            <CheckCircledIcon className="h-4 w-4" />
            <p>
              Result: <b>{result}</b>
            </p>
          </div>
        )}
        {error && (
          <div className="bg-red-500/15 p-3 rounded-md flex items-center gap-x-2 text-sm text-red-500">
            <ExclamationTriangleIcon className="h-4 w-4" />
            <p>
              Invalid Expression: <b>{error}</b>
            </p>
          </div>
        )}
      </>
    );
  }
);

export default ReversePolishNotationPushdownAutomaton;

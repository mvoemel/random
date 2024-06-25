import { useEffect, useRef, useState } from "react";
import ReversePolishNotationPushdownAutomaton, { RPNUPN_Ref } from "./RPNUPN";
import ComboBox from "./Combobox";

function App() {
  const STANDARD_OPTIONS = [
    "", // DEFAULT
    "34+62+89+43+***", // Result: 6664
    "31+78+987+1214++7++++++", // Result: 58
    "11+", // Result: 2
    "4", // Result: 4
    "22+22++", // Result: 8
    "333++", // Result: 9
    "1111*++", // Result: 3
    "34+*", // Result: Invalid
    "8+9+7*2*", // Result: Invalid
    "23+98+", // Result: Invalid
    "3*3", // Result: Invalid
    "+77", // Result: Invalid
  ];

  const [input, setInput] = useState(localStorage.getItem("RPNUPNinput") || "");
  const [stepMode, setStepMode] = useState(false);
  const [disabled, setDisabled] = useState(false);

  const ref = useRef<RPNUPN_Ref>(null);

  const enableStartButton = () => {
    setDisabled(false);
  };

  const updateRPNUPN = () => {
    setDisabled(true);
    ref.current?.runAnimation(input, stepMode);
  };

  useEffect(() => {
    localStorage.setItem("RPNUPNinput", input);
  }, [input]);

  return (
    <>
      <h1 className="mb-2 text-center">
        Reverse Polish Notation Pushdown Automaton
      </h1>
      <div className="flex flex-row items-center justify-center">
        <label className="mr-3">
          Input:{" "}
          <ComboBox
            options={STANDARD_OPTIONS}
            inputValue={input}
            setInputValue={setInput}
          />
        </label>
        <label className="mr-3">
          StepMode:{" "}
          <input
            type="checkbox"
            defaultChecked={stepMode}
            onChange={() => setStepMode(!stepMode)}
          />
        </label>
        <button onClick={updateRPNUPN} disabled={disabled}>
          Start
        </button>
      </div>
      <div className="flex flex-col items-center justify-center min-h-screen p-2">
        <ReversePolishNotationPushdownAutomaton
          ref={ref}
          enableStartButton={enableStartButton}
        />
      </div>
    </>
  );
}

export default App;

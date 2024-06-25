interface ComboBoxInterface {
  options: string[];
  inputValue: string;
  setInputValue: (newValue: string) => void;
}

const ComboBox = ({
  options,
  inputValue,
  setInputValue,
}: ComboBoxInterface) => {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(e.target.value);
  };

  const handleOptionClick = (option: string) => {
    setInputValue(option);
  };

  return (
    <div className="flex flex-col">
      <input
        type="text"
        value={inputValue}
        onChange={handleInputChange}
        placeholder="Enter expression..."
      />
      <select onChange={(e) => handleOptionClick(e.target.value)}>
        {options.map((option, index) => (
          <option key={index} value={option}>
            {option}
          </option>
        ))}
      </select>
    </div>
  );
};

export default ComboBox;

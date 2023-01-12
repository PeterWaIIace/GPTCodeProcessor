const {useState} = React;

let language_placeholder = "Python"

let prompt_components = {
    "prompt_start"            :"I want you to write program in Python. You are allowed to respond only in JSON. No explanation. No English text.\n"+
    "Program: Program generates and prints output\n",
    "init_prompt_input_reqs"  :"Program Input: ",
    "input_reqs"              : "No input\n",
    "init_prompt_output_reqs" : "Program Output: ",
    "output_reqs"             : "Hello World\n",
    "init_prompt_closing"     : "Respond with JSON having one field \"CODE\" with Python code."
};

function build_prompt()
{
    let prompt = "";
    for (const key in prompt_components)
    {
        prompt += prompt_components[key];
    };
    return prompt;
}

function CodeView()
{
    const [displayedText, setDisplayedText] = useState("");
    // // TO DO: make fetch request to local server
    setInterval(function() {
        fetch(`${window.location.origin}/read/dummy.py`, {cache: "no-store"})
        .then(response => response.text())
        .then(text     => setDisplayedText(text))
        .catch(error   => console.error('Error:', error));
    }, 1500);

    return (
        <div>
            <h2>Generated Code:</h2>
            <p style={{whiteSpace: 'pre'}}>{displayedText}</p>
        </div>
    );
};

function PromptInput()
{
    const [inputReqs, setInputReqs]   = useState(prompt_components["input_reqs"]);
    const [outputReqs, setOutputReqs] = useState(prompt_components["output_reqs"]);

    const handleOutputReqsChange = event => {
        // 👇️ access textarea value
        setOutputReqs(event.target.value);
        prompt_components["output_reqs"] = document.getElementById("output_reqs").textContent;
    };

    const handleInputReqsChange = event => {
        // 👇️ access textarea value
        setInputReqs(event.target.value);
        prompt_components["input_reqs"] = document.getElementById("input_reqs").textContent;
    };

    const onPressGenerate = event => {

        let prompt = build_prompt();
        prompt.replace(language_placeholder, document.getElementById("dLang").textContent);

        fetch(`${window.location.origin}/buttons/start`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({
                    "prompt":prompt,
                    "API": document.getElementById("dAPI").textContent
                })
            }
        ).catch(error   => console.error('Error:', error));
    }

    const onPressStop = event => {
        fetch(`${window.location.origin}/buttons/stop`,
            {
                method: 'POST'
            }
        ).catch(error   => console.error('Error:', error));
    }

    const onDropdownChoice = event =>
    {
        document.getElementById("dAPI").textContent = event.target.text;
    }

    return (
        <div>
            <div className="row">
                Language
                <div className="btn-group">
                    <button type="button" id="dLang" className="btn btn-primary m-1 dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        Python
                    </button>
                    <div className="dropdown-menu" aria-labelledby="dLabel">
                        <a className="dropdown-item" onClick={onDropdownChoice} href="#">Python</a>
                    </div>
                </div>
            </div>

            <div className="row">
                Input Code
                <textarea  style={{width: "100%",height: "100px"}}
                    type="text" id="input_reqs" name="fname" value={inputReqs} onChange={handleInputReqsChange}>
                </textarea>
                Output of Code
                <textarea  style={{width: "100%",height: "100px"}}
                    type="text" id="output_reqs" name="fname" value={outputReqs} onChange={handleOutputReqsChange}>
                </textarea>
            </div>

            <div className="row">
                <button onClick={onPressGenerate} className="btn btn-primary m-1" title="Send Prompt">Generate</button>
                <button onClick={onPressStop} className="btn btn-primary m-1" title="Send Prompt">Stop</button>

                <div className="btn-group">
                    <button type="button" id="dAPI" className="btn btn-primary m-1 dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        revChatGPT
                    </button>
                    <div className="dropdown-menu" aria-labelledby="dLabel">
                        <a className="dropdown-item" onClick={onDropdownChoice} href="#">revChatGPT</a>
                        <a className="dropdown-item" onClick={onDropdownChoice} href="#">OpenAIAPI</a>
                    </div>
                </div>
            </div>
        </div>
    );
};

function PromptResponse()
{
    const [displayedResponse, setDisplayedResponse] = useState("");
    // // TO DO: make fetch request to local server
    setInterval(function() {
        fetch(`${window.location.origin}/GPTresponse`)
        .then(response => response.text())
        .then(text     => setDisplayedResponse(text))
        .catch(error   => console.error('Error:', error));
    }, 1000);

    return (
        <div>
          <p style={{whiteSpace: 'pre'}}>{displayedResponse}</p>
        </div>
    );
};


ReactDOM.render(
    <div className="container">
        <div className="row">
            <div className="col-sm">
                <CodeView></CodeView>
            </div>
            <div className="col-sm">
                <PromptInput></PromptInput>
                <PromptResponse></PromptResponse>
            </div>
        </div>
    </div>
    ,document.getElementById('root')
);
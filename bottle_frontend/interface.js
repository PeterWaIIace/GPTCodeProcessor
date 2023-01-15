const {useState} = React;

let language_placeholder = "Python"

let prompt_parameters = {
    "functionDescription"      : "function do not take input and print output",
    "inputReqs"                : "No input\n",
    "outputReqs"               : "Hello world"
};


function CodeView()
{
    const [displayedText, setDisplayedText] = useState("");

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
    const [inputfunctionDescription, setfunctionDescription]   = useState(prompt_parameters["functionDescription"]);
    const [inputReqs, setInputReqs]   = useState(prompt_parameters["inputReqs"]);
    const [outputReqs, setOutputReqs] = useState(prompt_parameters["outputReqs"]);

    const handlefunctionDescriptionChange = event => {
        setfunctionDescription(event.target.value);
        prompt_parameters["functionDescription"] = event.target.value;
    }

    const handleOutputReqsChange = event => {
        // 👇️ access textarea value
        setOutputReqs(event.target.value);
        prompt_parameters["outputReqs"] = event.target.value;
    };

    const handleInputReqsChange = event => {
        // 👇️ access textarea value
        setInputReqs(event.target.value);
        prompt_parameters["inputReqs"] = event.target.value;
    };

    const onPressGenerate = event => {
        fetch(`${window.location.origin}/buttons/start`,
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                  },
                body: JSON.stringify({
                    "input":prompt_parameters["inputReqs"],
                    "output":prompt_parameters["outputReqs"],
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
                function Description
                <textarea  style={{width: "100%",height: "100px"}}
                    type="text" id="inputReqs" name="fname" value={inputfunctionDescription} onChange={handlefunctionDescriptionChange}>
                </textarea>
                Input description
                <textarea  style={{width: "100%",height: "100px"}}
                    type="text" id="inputReqs" name="fname" value={inputReqs} onChange={handleInputReqsChange}>
                </textarea>
                Output description
                <textarea  style={{width: "100%",height: "100px"}}
                    type="text" id="outputReqs" name="fname" value={outputReqs} onChange={handleOutputReqsChange}>
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
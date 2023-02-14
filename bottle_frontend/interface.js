const {useState,useEffect} = React;

let language_placeholder = "Python"

let prompt_parameters = {
    "functionDescription"      : "function do not take input and print output",
    "inputReqs"                : "No input\n",
    "outputReqs"               : "Hello world"
};


function CodeView()
{
    const [displayedText,  setDisplayedText] = useState("");
    const [displayedInput,  setDisplayedInput] = useState("");
    const [displayedOutput, setDisplayedOutput] = useState("");

    useEffect(() => {
        setInterval(function() {
            fetch(`${window.location.origin}/read/dummy.py`, {cache: "no-store"})
            .then(response => response.text())
            .then(text     => setDisplayedText(text))
            .catch(error   => console.error('Error:', error));

            fetch(`${window.location.origin}/readJson/raw.json`, { cache: "no-store", method: 'GET', headers: {'Content-Type': 'application/json', 'Accept': 'application/json',},})
            .then(response => response.json())
            .then(text     => {
                setDisplayedInput(text["Inputs"]);
                setDisplayedOutput(text["Outputs"]);
            })
        }, 1500);
    }, [])
    // setInterval(function() {

    // }, 1500);

    return (
        <div>
            <h2>Generated Code:</h2>
            <div className="form-outline">
                <textarea className="form-control" id="inputReqs" rows="17"  style={{ background: 'rgba(10,0,0,.5)'}} value={displayedText} readonly></textarea>
            </div>
            <h2>Test:</h2>
            <div className="row">
                <div className="col">
                    <h3>Inputs:</h3>
                    <div className="form-outline">
                        <textarea className="form-control" id="inputReqs" rows="2" style={{ background: 'rgba(10,0,0,.5)'}} value={displayedInput} readonly></textarea>
                    </div>
                </div>
                <div className="col">
                    <h3>Outputs:</h3>
                    <div className="form-outline">
                        <textarea className="form-control" id="inputReqs" rows="2" style={{ background: 'rgba(10,0,0,.5)'}} value={displayedOutput} readonly></textarea>
                    </div>
                </div>
            </div>
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
        <div className="col">
            <div className="row">
                <div className="col-3">
                    <h2>Language</h2>
                    <div className="btn-group col-4 m-1">
                        <button type="button" id="dLang" className="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
                            Python
                        </button>
                        <ul className="dropdown-menu" aria-labelledby="dLabel">
                            <li><a className="dropdown-item" onClick={onDropdownChoice} href="#">Python</a></li>
                        </ul>
                    </div>
                </div>

                <div className="col-3">
                    <h2>API</h2>
                    <div className="btn-group col-3 m-1">
                        <button type="button" id="dAPI" className="btn btn-primary dropdown-toggle" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        OpenAIAPI
                        </button>
                        <div className="dropdown-menu" aria-labelledby="dLabel">
                            <a className="dropdown-item" onClick={onDropdownChoice} href="#">revChatGPT</a>
                            <a className="dropdown-item" onClick={onDropdownChoice} href="#">OpenAIAPI</a>
                        </div>
                    </div>
                </div>
            </div>

            <div className="row">
                <h3>Input description</h3>
                <div className="form-outline">
                    <textarea className="form-control" id="inputReqs" rows="5"  value={inputReqs} onChange={handleInputReqsChange}></textarea>
                </div>
                <h3>Function description</h3>
                <div className="form-outline">
                    <textarea className="form-control" id="inputReqs" rows="5"  value={inputfunctionDescription} onChange={handlefunctionDescriptionChange}></textarea>
                </div>
                <h3>Output description</h3>
                <div className="form-outline">
                    <textarea className="form-control" id="outputReqs" rows="5"  value={outputReqs} onChange={handleOutputReqsChange}></textarea>
                </div>
            </div>

            <div className="row">
                <div className="col" align="left">
                    <button onClick={onPressGenerate} className="btn btn-primary m-1 mt-2 col-4" title="Send Prompt">Generate</button>
                    <button onClick={onPressStop} className="btn btn-primary m-1 mt-2 col-4" title="Send Prompt">Stop</button>
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
            <div className="col" align="center">
                <h1>CodeGenerator</h1>
            </div>
        </div>
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
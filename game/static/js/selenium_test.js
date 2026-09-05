function startSeleniumTest(button) {

    const testName = button.dataset.testName;

    const test = button.value;

    // Set modal title

    document.getElementById("seleniumModalLabel"
    ).textContent = testName;


    const status = document.getElementById("seleniumStatus");

    status.textContent = "STARTING";
    status.className = "badge bg-secondary ms-3";


    const output = document.getElementById("seleniumOutput");

    output.textContent =
        "Starting test...\n";


    document.getElementById(
        "seleniumCloseButton"
    ).disabled = true;


    const csrfToken =
        document.querySelector(
            "[name=csrfmiddlewaretoken]"
        ).value;


    fetch("/selenium_testrunner/", {

        method: "POST",

        headers: {
            "Content-Type":
                "application/x-www-form-urlencoded",

            "X-CSRFToken":
                csrfToken
        },

        body:
            "test=" +
            encodeURIComponent(test)

    })

    .then(response => response.json())
    
    .then(data => {

        console.log(
            "Started test:",
            data.test_id
        );

        checkTestStatus(data.test_id);

    })
    then.console.response.log("response", response)
    .catch(error => {

        console.error(error);

        status.textContent = "FIRST ERROR";
        status.className =
            "badge bg-danger ms-3";

        output.textContent +=
            "\nFIRST ERROR: " + error;

    });
}

function checkTestStatus(testId) {

    fetch(
        "/selenium_testrunner/status/" +
        testId +
        "/"
    )

    .then(response => response.json())

    .then(data => {

        const output =
            document.getElementById(
                "seleniumOutput"
            );

        const status =
            document.getElementById(
                "seleniumStatus"
            );


        // Display output

        output.textContent =
            data.output.join("\n");


        // Scroll to bottom

        output.scrollTop =
            output.scrollHeight;


        // Still running?

        if (data.status === "running") {

            status.textContent = "RUNNING";

            status.className =
                "badge bg-primary ms-3";


            // Ask again in 500ms

            setTimeout(
                () => checkTestStatus(testId),
                500
            );

        }


        // Passed

        else if (data.status === "passed") {

            status.textContent = "PASSED";

            status.className =
                "badge bg-success ms-3";

            document.getElementById(
                "seleniumCloseButton"
            ).disabled = false;

        }


        // Failed

        else if (data.status === "failed") {

            status.textContent = "FAILED";

            status.className =
                "badge bg-danger ms-3";

            document.getElementById(
                "seleniumCloseButton"
            ).disabled = false;

        }

    })

    .catch(error => {

        console.error(
            "Status request failed:",
            error
        );

    });
}
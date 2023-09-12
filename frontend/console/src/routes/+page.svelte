<script>
    let studentIdCreate = "";
    let nameCreate = "";
    let adminPasswordCreate = "";
    let responseMessageCreate = "";
    let errorMessageCreate = "";

    let studentIdAdd = "";
    let tokenToAdd = 0;
    let nameToAdd = "";

    let adminPasswordAdd = "";
    let responseMessageAdd = "";
    let errorMessageAdd = "";

    const server_url = "https://game.hees.academy";
    let isLoadingCreate = false;
    let isLoadingAdd = false;

    function createUser() {
        if (isLoadingCreate) return;

        isLoadingCreate = true;
        errorMessageCreate = "";

        responseMessageCreate = "";

        fetch(server_url + "/create_user", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                student_id: studentIdCreate,
                name: nameCreate,
                token_to_add: 0,
                admin_password: adminPasswordCreate,
            }),
        })
            .then(async (response) => {
                if (response.ok) {
                    const data = await response.json();
                    responseMessageCreate = data.message;
                } else {
                    const errorData = await response.json();
                    errorMessageCreate = errorData.detail || "Error creating user.";
                }
            })
            .catch((error) => {
                errorMessageCreate = "Error: " + error.message;
            })
            .finally(() => {
                isLoadingCreate = false;
            });
    }

    function addUserToken() {
        if (isLoadingAdd) return;

        isLoadingAdd = true;
        errorMessageAdd = "";

        responseMessageAdd = "";

        fetch(server_url + "/add_user_token", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                student_id: studentIdAdd,
                token_to_add: tokenToAdd,
                admin_password: adminPasswordAdd,
                name: nameToAdd,
            }),
        })
            .then(async (response) => {
                if (response.ok) {
                    const data = await response.json();
                    responseMessageAdd = `Remaining token: ${data.remain_token}`;
                    // responseMessageAdd = data.remain_token
                    //     ? `Remaining token: ${data.remain_token}`
                    //     : data.message || "Token added.";
                } else {
                    const errorData = await response.json();
                    errorMessageAdd = errorData.detail || "Error adding token.";
                }
            })
            .catch((error) => {
                errorMessageAdd = "Error: " + error.message;
            })
            .finally(() => {
                isLoadingAdd = false;
            });
    }

    function resetFields() {
        studentIdCreate = "";
        nameCreate = "";
        adminPasswordCreate = "";

        studentIdAdd = "";
        tokenToAdd = 0;
        nameToAdd = "";
        adminPasswordAdd = "";
    }
</script>

<div class="p-4">
    <h2 class="text-xl font-bold mb-4">Create User</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label class="mb-2">
            Student ID:
            <input type="number" class="border rounded p-2" bind:value={studentIdCreate}/>
        </label>
        <label class="mb-2">
            Name:
            <input type="text" class="border rounded p-2" bind:value={nameCreate}/>
        </label>
        <label class="mb-2">
            Admin Password:
            <input type="password" class="border rounded p-2" bind:value={adminPasswordCreate}/>
        </label>
    </div>
    <button
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50 mt-4"
            on:click={createUser}
            disabled={isLoadingCreate}
    >
        {#if isLoadingCreate}
            Creating User...
        {:else}
            Create User
        {/if}
    </button>

    <h2 class="text-xl font-bold mt-8 mb-4">Add User Token</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label class="mb-2">
            Student ID:
            <input type="number" class="border rounded p-2" bind:value={studentIdAdd}/>
        </label>
        <label class="mb-2">
            Name:
            <input type="text" class="border rounded p-2" bind:value={nameToAdd}/>
        </label>
        <label class="mb-2">
            Tokens to Add:
            <input type="number" class="border rounded p-2" bind:value={tokenToAdd}/>
        </label>
        <label class="mb-2">
            Admin Password:
            <input type="password" class="border rounded p-2" bind:value={adminPasswordAdd}/>
        </label>
    </div>
    <button
            class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded disabled:opacity-50 mt-4"
            on:click={addUserToken}
            disabled={isLoadingAdd}
    >
        {#if isLoadingAdd}
            Adding Token...
        {:else}
            Add Token
        {/if}
    </button>

    <br/>

    <button
            class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded mt-4"
            on:click={resetFields}
    >
        Reset Fields
    </button>

    <h2 class="text-xl font-bold mt-8 mb-4">Response</h2>

    <div class="mt-8">
        <p class="text-lg font-semibold">Create User Response:</p>
        <pre class="bg-gray-200 p-2 rounded">{responseMessageCreate}</pre>
    </div>

    <div class="mt-4">
        <p class="text-lg font-semibold">Add User Token Response:</p>
        <pre class="bg-gray-200 p-2 rounded">{responseMessageAdd}</pre>
    </div>

    {#if errorMessageCreate || errorMessageAdd}
        <h2 class="text-xl font-bold mt-8 mb-4">Error</h2>
    {/if}

    {#if errorMessageCreate}
        <p class="text-red-600 mt-4" style="color: red">Create User
            Error: {errorMessageCreate || "An unknown error occurred."}</p>
    {/if}

    {#if errorMessageAdd}
        <p class="text-red-600 mt-4" style="color: red">Add User Token
            Error: {errorMessageAdd || "An unknown error occurred."}</p>
    {/if}
</div>
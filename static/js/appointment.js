function validate(val) {
    var v1 = document.getElementById("fname");
    var v2 = document.getElementById("lname");
    var v3 = document.getElementById("email");
    var v4 = document.getElementById("mob");
    var v5 = document.getElementById("subject");
    var v6 = document.getElementById("ans");

    var flag1 = true;
    var flag2 = true;
    var flag3 = true;
    var flag4 = true;
    var flag5 = true;
    var flag6 = true;

    if (val >= 1 || val == 0) {
        if (v1.value === "") {
            v1.style.borderColor = "red";
            flag1 = false;
        } else {
            v1.style.borderColor = "green";
            flag1 = true;
        }
    }

    if (val >= 2 || val == 0) {
        if (v2.value === "") {
            v2.style.borderColor = "red";
            flag2 = false;
        } else {
            v2.style.borderColor = "green";
            flag2 = true;
        }
    }

    if (val >= 3 || val == 0) {
        if (v3.value === "") {
            v3.style.borderColor = "red";
            flag3 = false;
        } else {
            v3.style.borderColor = "green";
            flag3 = true;
        }
    }

    if (val >= 4 || val == 0) {
        if (v4.value === "") {
            v4.style.borderColor = "red";
            flag4 = false;
        } else {
            v4.style.borderColor = "green";
            flag4 = true;
        }
    }

    if (val >= 5 || val == 0) {
        if (v5.value === "") {
            v5.style.borderColor = "red";
            flag5 = false;
        } else {
            v5.style.borderColor = "green";
            flag5 = true;
        }
    }

    if (val >= 6 || val == 0) {
        if (v6.value === "") {
            v6.style.borderColor = "red";
            flag6 = false;
        } else {
            v6.style.borderColor = "green";
            flag6 = true;
        }
    }

    var flag = flag1 && flag2 && flag3 && flag4 && flag5 && flag6;

    return flag;
}


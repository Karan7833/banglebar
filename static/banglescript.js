
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const eye = document.getElementById('eyebtn');  // Eye icon ka id

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        eye.classList.remove('fa-eye-slash');
        eye.classList.add('fa-eye');
    } else {
        passwordInput.type = 'password';
        eye.classList.remove('fa-eye');
        eye.classList.add('fa-eye-slash');
    }
}

function checklogin() {
    const userData = {
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Login Successful!");
            window.location.href = "/";  // login ke baad redirect
        } else {
            alert("Invalid email or password!");
        }
    })
    .catch(error => {
        console.error("Login error:", error);
        alert("Something went wrong during login.");
    });
}





    // Data object
document.getElementById('signupForm').addEventListener('submit', function(e) {
    e.preventDefault(); // default submit rok dega

    // Data object yaha lo
    const userData = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value, 
        password: document.getElementById('password').value
    };

    // Ab fetch yaha call karo
    fetch('/signup', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => response.json())
.then(data => {
    if (data.success) {
        window.location.href = "/"; // ✅ redirect frontend se
    } else {
        alert('Error: ' + data.message);
    }
          })

    .catch(error => {
        console.error('Signup error:', error);
        alert('Something went wrong during signup.');
    });
});


// Add to cart functionality
function addcart() {
    let cartItem = document.getElementById("addcart"); 
    if (cartItem) {
        alert("Item added to cart!");
        // Future: yaha backend ko call kar sakte ho to save cart in DB
    } else {
        console.error("Add to cart element not found");
    }
}


  // Newsletter demo
  function bbSubscribe(e){
    e.preventDefault();
    const i=e.target.querySelector('input[type="email"]');
    if(!i) return false;
    alert("Thanks for subscribing, " + i.value + " ✨");
    i.value="";
    return false;
  }
  // Year
  document.getElementById("bb-year").textContent = new Date().getFullYear();

 
  function openTerms() {
    document.getElementById("termsModal").style.display = "block";
  }
  function closeTerms() {
    document.getElementById("termsModal").style.display = "none";
  }
  function acceptTerms() {
    document.getElementById("terms").disabled = false;
    document.getElementById("terms").checked = true;
    closeTerms();
  }

  // Optional: form validation safety
  document.getElementById("signupForm").addEventListener("submit", function(e){
    if (!document.getElementById("terms").checked) {
      e.preventDefault();
      alert("Please accept Terms & Conditions to continue.");
    }
  });


  

    // Search functionality

    const searchInput = document.getElementById("searchInput");
    const productList = document.getElementById("productList");
    const products = productList.getElementsByClassName("product");

    searchInput.addEventListener("keyup", function() {
      const filter = searchInput.value.toLowerCase();

      for (let i = 0; i < products.length; i++) {
        let text = products[i].textContent || products[i].innerText;
        if (text.toLowerCase().indexOf(filter) > -1) {
          products[i].style.display = "";
        } else {
          products[i].style.display = "none";
        }
      }
    });

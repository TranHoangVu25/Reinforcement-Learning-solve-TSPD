// let btn_q = document.getElementById('btn_q')
// let btn_sarsa = document.getElementById('btn_sarsa')
//     btn_q.addEventListener('click',function(){
//   // Gửi yêu cầu GET đến API Python
 
//     })

//     btn_sarsa.addEventListener('click',function(){

//     })
    let run_q = document.getElementById('run_q')
    run_q.addEventListener('click',function(){
        const statusMessage = document.getElementById('statusMessage');
        const userConfirmed = confirm("Do you want to run program?");

if (userConfirmed) {
    statusMessage.textContent = "Processing...";

    setTimeout(() => {
        fetch("http://127.0.0.1:5000/api/run_program", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    statusMessage.textContent = "Run successfully!";
                } else {
                    statusMessage.textContent = "Error: " + data.error;
                }
            })
            .catch(error => {
                statusMessage.textContent = "Lỗi kết nối tới server: " + error.message;
            });
            fetch('/api/result_q')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
            .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('Truck_route_q').innerHTML = data.result.join(' -> ');
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });

fetch('/api/result_q_drone')
    .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
            .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('Drone_route_q').innerHTML = data.result.join(' -> ');
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
fetch('/api/emissions_q')
    .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
            .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('emissions_q').innerHTML = data.result.join(' -> ');
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
fetch('/api/result_sarsa_drone')
    .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
    .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('Drone_route_sarsa').innerHTML = data.result.join(' -> ');
            })
    .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    
fetch('/api/result_sarsa_truck')
    .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
    .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('Truck_route_sarsa').innerHTML = data.result.join(' -> ');
            })
    .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });    

fetch('/api/emissions_sarsa')
    .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json(); // Chuyển đổi kết quả API sang JSON
            })
            .then(data => {
                // Lấy dữ liệu từ API và hiển thị lên giao diện
                document.getElementById('emissions_sarsa').innerHTML = data.result.join(' -> ');
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }); // Delay 2 giây
} else {
    // Người dùng nhấn "Cancel"
    statusMessage.textContent = "Program run canceled.";
}
    })

async function fetchImage_truck_q(filename) {
    try {
        // Gửi yêu cầu GET đến Flask API
        const response = await fetch(`/api/get_image/${filename}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Tạo thẻ <img> để hiển thị ảnh
        const imgElement = document.createElement('img');
        imgElement.src = response.url; // Đường dẫn URL của ảnh
        imgElement.alt = filename; // Thuộc tính alt cho ảnh
        imgElement.style.maxWidth = '100%'; // Định dạng ảnh (tùy chọn)

        // Gắn thẻ <img> vào container
        const container = document.getElementById('image_container_truck_q');
        container.innerHTML = ''; // Xóa nội dung cũ
        container.appendChild(imgElement); // Thêm ảnh mới
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}

async function fetchImage_drone_q(filename) {
    try {
        // Gửi yêu cầu GET đến Flask API
        const response = await fetch(`/api/get_image/${filename}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Tạo thẻ <img> để hiển thị ảnh
        const imgElement = document.createElement('img');
        imgElement.src = response.url; // Đường dẫn URL của ảnh
        imgElement.alt = filename; // Thuộc tính alt cho ảnh
        imgElement.style.maxWidth = '100%'; // Định dạng ảnh (tùy chọn)

        // Gắn thẻ <img> vào container
        const container = document.getElementById('image_container_drone_q');
        container.innerHTML = ''; // Xóa nội dung cũ
        container.appendChild(imgElement); // Thêm ảnh mới
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}

async function fetchImage_truck_sarsa(filename) {
    try {
        // Gửi yêu cầu GET đến Flask API
        const response = await fetch(`/api/get_image/${filename}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Tạo thẻ <img> để hiển thị ảnh
        const imgElement = document.createElement('img');
        imgElement.src = response.url; // Đường dẫn URL của ảnh
        imgElement.alt = filename; // Thuộc tính alt cho ảnh
        imgElement.style.maxWidth = '100%'; // Định dạng ảnh (tùy chọn)

        // Gắn thẻ <img> vào container
        const container = document.getElementById('image_container_truck_sarsa');
        container.innerHTML = ''; // Xóa nội dung cũ
        container.appendChild(imgElement); // Thêm ảnh mới
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}

async function fetchImage_drone_sarsa(filename) {
    try {
        // Gửi yêu cầu GET đến Flask API
        const response = await fetch(`/api/get_image/${filename}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Tạo thẻ <img> để hiển thị ảnh
        const imgElement = document.createElement('img');
        imgElement.src = response.url; // Đường dẫn URL của ảnh
        imgElement.alt = filename; // Thuộc tính alt cho ảnh
        imgElement.style.maxWidth = '100%'; // Định dạng ảnh (tùy chọn)

        // Gắn thẻ <img> vào container
        const container = document.getElementById('image_container_drone_sarsa');
        container.innerHTML = ''; // Xóa nội dung cũ
        container.appendChild(imgElement); // Thêm ảnh mới
    } catch (error) {
        console.error('Error fetching image:', error);
    }
}
document.getElementById('load-image-btn').addEventListener('click', function () {
    fetchImage_truck_q('truck_route_qlearning.png'); // Thay tên file bằng file bạn muốn hiển thị
    fetchImage_drone_q('drone_route_qlearning.png');
    
});
document.getElementById('load-image-btn1').addEventListener('click',function(){
    fetchImage_truck_sarsa('truck_route_SARSA.png');
    fetchImage_drone_sarsa('drone_route_SARSA.png');
})
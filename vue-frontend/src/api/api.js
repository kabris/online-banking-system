import axios from 'axios';

VUE_APP_API_URL='http://127.0.0.1:5000'


export const loginUser = async (email, password) => {
    return axios.post(`${BASE_URL}/api/login`, { email, password });
    axios.post('http://localhost:5000/api/login', data)

};

export const fetchUserData = async (userId) => {
    return axios.get(`${BASE_URL}/api/user/${userId}`);
};

export const uploadFile = async (formData) => {
    return axios.post(`${BASE_URL}/api/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    });
};

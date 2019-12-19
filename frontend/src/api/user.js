import axios from './http';
import qs from 'qs'

const user = {
  //用户注册
  register(params){
    return axios.post('/api/register', qs.stringify(params))
  },
  //用户登录
  login(params){
    return axios.post('/api/login', qs.stringify(params))
  },
  //修改用户信息
  alterMessage(params){
    return axios.post('/api/alterMessage', qs.stringify(params))
  },
  //获取用户信息
  getMessage(params){
    return axios.post('/api/getMessage', qs.stringify(params))
  },
  //！添加进购物篮
  addBasket(params) {
    return axios.post('/api/addBasket', qs.stringify(params))
  },
  //！取消购物篮中的记录
  DeleteBasketMessage(params){
    return axios.post('/api/DeleteBasketMessage', qs.stringify(params))
  },
  //！获取用户购物篮
  getBasketMessage(params){
    return axios.post('/api/getBasketMessage', qs.stringify(params))
  },
  //上传图片
  upLoadImage(params, config){
    return axios.post('/api/upLoadImage', params, config)
  },
  //获取图片链接
  getImage(params){
    return axios.post('/api/getImage', qs.stringify(params))
  },

  //！报表记录
  addSalesRecord(params){
    return axios.post('/api/addSalesRecord', qs.stringify(params))
  },
  //！日志记录
  addLog(params){
    return axios.post('/api/addLog', qs.stringify(params))
  },

  // ！发邮件
  send_email(params){
    return axios.post('/api/send_email', qs.stringify(params))
  },
}

export default user;

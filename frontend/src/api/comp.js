import axios from './http';
import qs from 'qs'

const comp = {
  //！获取单个商品信息
  getComdyInfoById(params){
    return axios.post('/api/getComdyInfoById', qs.stringify(params))
  },
  // ！获取商品，按类别
  getComdyInfoByClassId(params){
    return axios.post('/api/getComdyInfoByClassId', qs.stringify(params))
  },
}

export default comp;

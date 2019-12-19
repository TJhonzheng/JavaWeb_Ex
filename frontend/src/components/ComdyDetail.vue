<template>
  <div class="comdyInfo">

      <img :src="imgUrl" class="avatar">

    <el-form ref="form" label-width="70px">
      <el-row>
        <el-col style="margin-top: 20px; margin-left: 20px; margin-right: 20px;">
          <h2 style="margin-right: 20px;">{{this.name}}</h2>
        </el-col>
      </el-row>

      <el-row>
        <el-col :span="10">
          <el-form-item label="价格" prop="price">
            <el-tag type="danger">{{this.price}}</el-tag>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="发货地" prop="area">
          <el-tag>{{this.area}}</el-tag>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="10">
          <el-form-item label="销售量" prop="pCount">
            <el-tag>{{this.pCount}}</el-tag>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="库存量" prop="count">
            <el-tag >{{this.count}}</el-tag>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="状态" prop="state">
        <el-tag type="success">{{this.state}}</el-tag>
      </el-form-item>


      <el-form-item label="详情" prop="statement">
        <el-input type="textarea" v-model="this.statement"  autocomplete="off" :disabled="!judge" autosize></el-input>
      </el-form-item>
    </el-form>
  </div>

</template>

<script>
    export default {
        name: "ComdyDetail",
        props:{
            userId:{
                type:Number
            },
            comdyId:{
                type: Number
            }
        },
        data(){
            return{
                info: '',
                id: '',
                name: '',
                price: '',
                imgUrl: '',
                area: '',
                state: '',
                pCount: '',
                count: '',
                statement: '',
                judge:false,
            }
        },
        mounted: function () {
            this.$api.comp.getComdyInfoById({
                comdyId:parseInt(this.comdyId)
            }).then(res=> {
                if(res.data.status==0){
                    let info = res.data.comdyInfo
                    this.cid = info['Cid']
                    this.name = info['CName']
                    this.price = info['CPrice']
                    this.imgUrl = info['CImg']
                    this.area = info['Area']
                    this.state = info['CState']
                    this.pCount = info['CPurchasesCount']
                    this.count = info['CCount']
                    this.statement = info['CStatement']
                }else {
                    this.$message.error(res.data.message)
                }
            })
        },
    }
</script>

<style lang="scss">
  .comdyInfo{

    .avatar {
      margin-left: 15%;
      width: 70%;
      height: 70%;
      display: block;
      right: 0;
      border-radius:15px;
      border-bottom:7px solid #ffecec;
      border-left:7px solid #ffecec;
      border-top:2px solid #ffeeee;
      border-right:2px solid #ffeeff;
    }
    .buttonGroup{
      display:flex;
      justify-content: center;
      align-items: center;
      flex-direction: row;
      .el-button{
        width:30%;
        border-radius: 30px;
      }
    }
    .el-tag{
      font-size:15px;
    }
  }
</style>

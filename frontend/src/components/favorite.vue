<template>
    <div v-if="basket==true" >
      <el-table :data="tableData.slice((currentPage-1)*PageSize,currentPage*PageSize)">
        <el-table-column
          prop="comdyName"
          label="商品名称" width="250px"></el-table-column>
        <el-table-column
          prop="comdyCount"
          label="购买数量"
        width="200px">
          <template scope="scope">
            <el-input-number style="width: 150px;" @change="countChange" v-model="scope.row.comdyCount" :min="1" :max="5"></el-input-number>
          </template>
        </el-table-column>
        <el-table-column
          label="商品总价">
          <template slot-scope="scope">
            {{scope.row.comdyP}}
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          prop="comdyId"
          width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="gotoPayment(scope.row.comdyId, scope.row.comdyCount, scope.row.comdyP, scope.row.comdyName)">付款</el-button>
            <el-button type="text" @click="deleteBasetMessage(scope.row.comdyId)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="tabListPage">
        <el-pagination @size-change="handleSizeChange"
                       @current-change="handlesCurrentChange"
                       :current-page="currentPage"
                       :page-sizes="pageSizes"
                       :page-size="PageSize" layout="total, prev, pager, next, jumper"
                       :total="totalCount">
        </el-pagination>
      </div>
    </div>
  <div v-else style="text-align: center">
      <span style="font-size: 30px; font-weight: 600;">付款码<br></span>
      <img src="../static/img/pay.png" width="400px" height="400px">
  </div>

</template>

<script>
    export default {
      name: "favorite",
      props:{
        userId:{
          type:Number
        },
          userName:{
            type: String
          }
      },
      mounted(){
        this.$api.user.getBasketMessage({
          userId:this.userId
        }).then((res)=>{
          console.log(res.data)
          if(res.data.status==0){
            let info = res.data.basketMessages
            this.totalCount = info.length
            for(let i=0;i<info.length;++i){
              this.tableData.push({
                comdyId:info[i]['comdyInfoId'],
                comdyName:info[i]['name'],
                  comdyCount:info[i]['count'],
                  comdyP:info[i]['price']*info[i]['count'],
                  comdyP_s:info[i]['price']
              })
            }
          }
        })
      },
      data(){
        return{
          tableData:[],
          currentPage:1,
          totalCount:0,
          PageSize:8,
          pageSizes:[1,2,3,4],
            basket: true
        }
      },
      methods:{
          countChange(value){
              this.tableData.forEach((ele, i) => {
                  ele.comdyP = ele.comdyCount * ele.comdyP_s
              })
          },
        // 每页显示的条数
        handleSizeChange(val) {
          // 改变每页显示的条数
          this.PageSize=val
          // 注意：在改变每页显示的条数时，要将页码显示到第一页
          this.currentPage=1
        },
        // 显示第几页
        handlesCurrentChange(val) {
          // 改变默认的页数
          this.currentPage=val
        },
          deleteBasetMessage(comdyId, success=false){
          this.$api.user.DeleteBasketMessage({
            comdyId:comdyId,
            userId:this.userId
          }).then((res)=>{
           if(res.data.status==0){
               for(let i=0;i<this.tableData.length;++i){
                   if(this.tableData[i]['comdyId']==comdyId){
                       this.tableData.splice(i, 1)
                       this.totalCount = this.totalCount - 1
                       break;
                   }
               }
               this.$emit('childsay', 1)
               if(success)
                  this.$message.success("支付成功")
               else
                  this.$message.success(res.data.message)
           }
           else{
             this.$message.error(res.data.message)
           }
          })
        },
          gotoPayment(Id, count, p, name){
              this.$message.success('下单成功！邮件已发送到您的邮箱。')
              this.basket = false;
              // 记录销售报表
              this.$api.user.addSalesRecord({
                  comdyId:Id,
                  userId:this.userId,
                  count: count,
                  totalAmount: p
              }).then((res)=> {
                  if(res.data.status==0) {
                      console.log("报表添加记录成功")
                  }else{
                      console.log("报表添加记录失败")
                  }
              })
              // 记录购买日志
              this.$api.user.addLog({
                  comdyId:Id,
                  userId:this.userId,
                  Statement: "用户："+this.userName+" 下单了商品：【"+ name.slice(0,26)+"...】 一共支付金额："+p+"元。"
              }).then((res)=> {
                  if(res.data.status==0) {
                      console.log("日志记录成功")
                  }else{
                      console.log("日志记录失败")
                  }
              })
              // 发邮件
              this.$api.user.send_email({
                  comdyId:Id,
                  userId:this.userId,
                  totalAmount: p
              }).then((res)=> {
                  if(res.data.status==0) {
                      console.log("邮件发送成功")
                  }else{
                      console.log("邮件发送失败")
                  }
              })
              this.deleteBasetMessage(Id, true)
        }
      }
    }
</script>

<style scoped>

</style>

<template>
  <div>
    <el-dialog title="商品详情"
               :visible.sync="comdyDetailVisible"
               v-if="comdyDetailVisible===true"
               append-to-body
               customClass="customWidth"
               width="100%"
    >
      <ComdyDetail :userId=userId :comdyId=showWhichComdy></ComdyDetail>
    </el-dialog>

    <div>
      <el-row style="height: 840px;">
        <el-input style="width: 400px; margin-bottom: 35px;"
                  v-model= "search"
                  placeholder="输入关键字搜索"></el-input>
        <el-table-column align="center">
        </el-table-column>
        <el-tooltip  placement="right"
                     v-for="item in tables.slice((currentPage-1)*pagesize,currentPage*pagesize)"
                     :key="item.cid">

          <p slot="content" style="font-size: 14px;margin-bottom: 6px">
            <span>{{item.name}}<br></span>
            <span>价格：{{item.price}}</span>
          </p>
          <p slot="content" style="width: 300px" class="abstract">{{item.abs}}</p>
          <el-card style="width: 205px;margin-bottom: 40px;height: 293px;float: left;margin-right: 35px;text-align:right;" class="book"
                   bodyStyle="padding:12px" shadow="hover">
            <div class="cover" @click="gotoDetails(item.cid, item.name)">
              <img :src="item.img" alt="图片">
            </div>
            <div style="height: 30px; margin-bottom: 10px;">
              <div class="title">
                <a href="">{{item.name}}</a>
              </div>
              <i class="el-icon-goods" style="margin-top: 14px; font-size: 20px;font-weight:800;" @click="mark(item.cid)"></i>
            </div>
            <div class="price">￥{{item.price}}</div>


          </el-card>
        </el-tooltip>
      </el-row>
      <el-row>
        <el-pagination
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-size="pagesize"
          :total="tables.length">
        </el-pagination>
      </el-row>
    </div>
  </div>


</template>

<script>
  import ComdyDetail from "./ComdyDetail";
    export default {
        name: 'comdyInfo',
        components: {ComdyDetail},
        data () {
            return {
                comdys: [],
                currentPage: 1,
                pagesize: 17,
                comdyIndex: 0,
                search:'',
                username:null,
                nickName:'',
                userId:'',
                showWhichComdy: 0,
                comdyDetailVisible: false
            }
        },
        computed: {
            tables () {
                const search = this.search
                if (search) {
                    console.log('this.comdys!!!', this.comdys)
                    return this.comdys.filter(dataNews => {
                        return Object.keys(dataNews).some(key => {
                            return String(dataNews[key]).toLowerCase().indexOf(search) > -1
                        })
                    })
                }
                console.log('this.comdys', this.comdys)
                return this.comdys
            }
        },
        mounted: function () {
            console.log(this.$route.params.classNum)
            if(this.$route.params.classNum)
                this.comdyIndex = this.$route.params.classNum
            this.username = sessionStorage.getItem('username')
            this.userId = parseInt(sessionStorage.getItem('userId'))
            this.nickName = sessionStorage.getItem('nickName')
            if(!this.nickName)
                this.nickName = this.username
            this.email = sessionStorage.getItem('email')

            this.$api.comp.getComdyInfoByClassId({
                classId:parseInt(this.comdyIndex)
            }).then(res=>{
                if(res.data.status==0){
                    console.log(res.data)
                    let infos = res.data.comdyInfo
                    this.totalCount = infos.length
                    for(let i=0;i<infos.length;++i){
                        let cid_ = infos[i]['Cid']
                        let name_ = infos[i]['CName']
                        let price_ = infos[i]['CPrice']
                        let img_ = infos[i]['CImg']
                        this.comdys.push({
                            cid: cid_,
                            name: name_.slice(0,26),
                            price: price_,
                            img: img_
                        })
                    }
                }
                else{
                    this.$message.error(res.data.message)
                }
            })
        },
        methods: {
            handleCurrentChange: function (currentPage) {
                this.currentPage = currentPage
            },
            mark (id) {
                if(!this.userId){
                    this.$message.warning('登录后才可以购买哦！')
                    return
                }
                this.$api.user.addBasket({
                    comdyId: id,
                    userId: this.userId
                }).then(res=> {
                    if(res.data.status==0){
                        this.favor+=1
                        this.$message.success('添加成功！')
                    }
                    else if(res.data.status==2){
                        this.$message.warning(res.data.message)
                    }
                    else{
                        this.$message.error('添加失败，请重试！')
                    }
                })
            },
            gotoDetails(id, name){
                this.showWhichComdy = id
                this.comdyDetailVisible = true
                this.$api.user.addLog({
                    comdyId:id,
                    userId:this.userId,
                    Statement: "用户："+this.username+" 浏览了商品：【"+ name.slice(0,30)+"...】"
                }).then((res)=> {
                    if(res.data.status==0) {
                        console.log("日志记录成功")
                    }else{
                        console.log("日志记录失败")
                    }
                })
            }

        },

    }
</script>
<style scoped>

  .cover {
    width: 185px;
    height: 172px;
    margin-bottom: 7px;
    overflow: hidden;
    cursor: pointer;
  }

  img {
    width: 100%;
    height: 172px;
    /*margin: 0 auto;*/
  }

  .title {
    font-size: 15px;
    text-align: left;
  }

  .price {
    color: #2c3e50;
    width: 82px;
    margin-right: 10px;
    font-weight: 700;
    font-size: 17px;
    margin-top: 22px;
    margin-left: 10px;
    text-align: left;
  }

  .abstract {
    display: block;
    line-height: 17px;
  }

  .el-icon-goods {
    cursor: pointer;
    float: right;
    margin-top: 12px;
  }

  .switch {
    display: flex;
    position: absolute;
    left: 780px;
    top: 25px;
  }

  a {
    text-decoration: none;
  }

  a:link, a:visited, a:focus {
    color: #3377aa;
  }

</style>

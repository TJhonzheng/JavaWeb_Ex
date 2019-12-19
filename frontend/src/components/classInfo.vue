<template>
    <div class="classInfo">
      <site-header></site-header>
      <div class="body">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="0" @click="gotoIndex">HOME</el-menu-item>
          <el-menu-item index="1" @click="gotoClassInfo('1')">游戏本</el-menu-item>
          <el-menu-item index="2" @click="gotoClassInfo('2')">轻薄本</el-menu-item>
          <el-menu-item index="3" @click="gotoClassInfo('3')">商务本</el-menu-item>
          <el-menu-item index="4" @click="gotoClassInfo('4')">台式机</el-menu-item>
        </el-menu>
        <div class="select"></div>

        <div style="margin-left: 50px;margin-right: 50px; margin-top: 50px;">
          <comdyInfo></comdyInfo>
        </div>


      </div>
    </div>
</template>

<script>
  import userInfo from './userInfo'
  import siteHeader from './siteHeader'
  import comdyInfo from "./comdyInfo";
    export default {
    components:{userInfo, siteHeader, comdyInfo},
        name: "classInfo",
      mounted(){
      console.log(this.$route.params.classNum)
        if(this.$route.params.classNum)
          this.activeIndex = this.$route.params.classNum
        this.username = sessionStorage.getItem('username')
        this.userId = sessionStorage.getItem('userId')
        this.nickName = sessionStorage.getItem('nickName')
        if(!this.nickName)
          this.nickName = this.username
          this.email = sessionStorage.getItem('email')
      },
      data(){
      return{
        userInfoVisible:false,
        activeIndex:"-1",
        username:null,
        nickName:'',
        userId:'',
        tableData:[],
        currentPage:1,
        totalCount:0,
        PageSize:8,
        pageSizes:[1,2,3,4],
        gameLevel:0,
        gameArea:0,
        selectStart:null,
        selectEnd:null,
        search:''
      }
      },
      computed: {
        tables () {
          const search = this.search
          if (search) {
            console.log('this.tableData', this.tableData)
            return this.tableData.filter(dataNews => {
              return Object.keys(dataNews).some(key => {
                return String(dataNews[key]).toLowerCase().indexOf(search) > -1
              })
            })
          }
          console.log('this.tableData', this.tableData)
          return this.tableData
        }
      },
      methods:{
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
      gotoClassInfo(classNum){
        // this.activeIndex = classNum
        this.$router.push({path:'/classInfo/'+classNum})
        this.$router.go(0)
      },
        gotoIndex(){
        this.$router.push({name:'index'})
        },
        handleSelect(key, keyPath) {
          // console.log(key, keyPath);
        },
        gotoCommunity(){
          this.$router.push({name:'community'})
        },
        logout(){
          sessionStorage.clear();
          this.$store.dispatch('UserLogout')
          if(! this.$store.state.token){

            this.$router.go(0)
          }else{
            this.$message.error('退出失败');
          }
        },
        openDetails(row){
          this.$router.push({path:'/gameDetail/'+row.gameName['gameId']})
        },
        select(){
          console.log(this.selectEnd)
          if(this.selectStart!=null&&this.selectEnd!=null&&this.selectEnd<this.selectStart)
          {
            this.$message.error('请正确选择时间！')
            return
          }
          let start = this.selectStart
          let end = this.selectEnd
          if(start==null)
            start = ''
          if(end==null)
            end = ''
          this.$api.comp.getCompInfoBySelect({
            gameClass:this.activeIndex,
            gameLevel: this.gameLevel,
            gameArea:this.gameArea,
            selectStart:start,
            selectEnd: end
          }).then((res)=>{
            if(res.data.status==0){
              let infos = res.data.compInfo
              this.tableData = []
              this.totalCount = infos.length
              for(let i=0;i<infos.length;++i){
                let gameName = infos[i]['IName']
                let gameId = infos[i]['Iid']
                let gameApplyEndTime = infos[i]['IApplyEndTime']
                let gameApplyStartTime = infos[i]['IApplyStartTime']
                this.tableData.push({
                  gameName:gameName,
                  gameId:gameId,
                  deltaTime:gameApplyEndTime,
                  startTime:gameApplyStartTime
                })
              }
              this.$message.success(res.data.message)
            }
            else{
              this.$message.error(res.data.message)
            }
          })
        }
      }
    }
</script>

<style lang="scss">
  .customWidth{
    width:40%!important;
  }
  .el-button{
    border-radius:30px;
  }

  .body{
    width:100%;
    margin:0;
    padding:0;
    .select{
      margin-top:220px;
      width:56%;
      margin-left:22%;
      .el-radio-group{
        display:flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row;
      }
      div{
        margin-bottom:14px;
      }
      .selectSon{
        margin-bottom:20px;
        display:flex;
        justify-content: space-between;
        align-items: center;
        flex-direction: row;
      }
      .el-button{
        width:60%;
        border-radius:50px;
      }
    }
    .el-menu{
      position:fixed;
      left:0;
      top:100px;
      width:100%;
      z-index:10;
      li{
        font-size:17px;
      }
    }
    .el-table{
      margin-top:20px;
      .el-input__inner{
        border-radius: 30px;
      }
    }
  }
</style>

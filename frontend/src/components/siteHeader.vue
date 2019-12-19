<template>
    <div class="header">
      <el-dialog title="我的信息"
                 :visible.sync="userInfoVisible"
                 v-if="userInfoVisible===true"
                 append-to-body
                 customClass="customWidth"
                 width="100%"
                 >
        <userInfo v-on:childsay="listenChild" v-on:childsay1="changeImg"></userInfo>
      </el-dialog>

      <el-dialog title="我的购物篮"
                 :visible.sync="BasketVisible"
                 v-if="BasketVisible===true"
                 append-to-body
                 customClass="customWidth"
                 width="100%"
                  >
        <favorite :userId=userId :user-name=username v-on:childsay="listenChild1"></favorite>
      </el-dialog>

      <div class="header-left">
        <img src="../static/img/com.jpg" @click="this.$router.push({path:'/'})">
        <span>京西电脑商城</span>
      </div>
      <div class="header-right">
        <div class="user">
          <i class="el-icon-user" v-if="username==null"></i>
          <img v-else :src=imgurl class="headimg">
          <router-link :to="{ path: '/login'}" replace v-if="username==null"><span>登录</span></router-link>
          <el-divider direction="vertical" v-if="username==null"></el-divider>
          <router-link :to="{ path: '/register'}" replace v-if="username==null"><span>注册</span></router-link>
          <div v-else>
            <el-dropdown>
              <span>  您好,{{nickName}}</span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="userInfoVisible=true">我的信息</el-dropdown-item>
                <el-dropdown-item @click.native="BasketVisible=true">我的购物篮</el-dropdown-item>
                <el-dropdown-item @click.native = "logout">登出</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
  import userInfo from './userInfo'
  import favorite from './favorite'
    export default {
      name: "siteHeader",
      components:{userInfo, favorite},
      mounted(){
        this.username = sessionStorage.getItem('username')
        this.userId = parseInt(sessionStorage.getItem('userId'))
        this.nickName = sessionStorage.getItem('nickName')
        this.imgurl = sessionStorage.getItem('imgurl')
          console.log("imgurl" + this.imgurl)
        if(!this.nickName)
          this.nickName = this.username
        this.email = sessionStorage.getItem('email')
        if(sessionStorage.getItem('is_superuser')==='false'||sessionStorage.getItem('is_superuser')==null)
          this.is_superuser = false
        else
          this.is_superuser = true
      },
      data(){
        return{
          userInfoVisible:false,

            BasketVisible:false,
          gamePublishVisible:false,
          username:null,
          nickName:'',
          userId:null,
          email:'',
          imgurl:'',
          is_superuser:false,
        }
      },
      methods:{
        logout(){
          sessionStorage.clear();
          this.$store.dispatch('UserLogout')
          if(! this.$store.state.token){
            this.$router.go(0)
          }else{
            this.$message.error('退出失败');
          }
        },
        listenChild:function(data){
          console.log('change')
          this.nickName = data
        },
        listenChild1:function(data){
          this.$emit('childsay', 1)
        },
        changeImg:function(data){
          this.imgurl = data
        }
      }
    }
</script>

<style lang="scss">
  .header{
    position: fixed;
    left:0px;
    top:0px;
    background-color: #ffeeee;
    width:100%;
    height:100px;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    z-index:10;

    .header-right{
      height:100%;
      width:20%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      a {
        text-decoration: none;
      }
      span{
        color:#2C537A
      }
      .user{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        .headimg{
          width:60px;
          height:60px;
          border-radius: 50%;
          margin-right:20px;
        }
        span{
          font-size:17px;
        }
      }
    }
    .header-left{
      height:100%;
      width:30%;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-around;
      img{
        width:110px;
        height:94%;
        margin-top:3%;
        margin-bottom:3%;
      }
      span{
        font-size:32px;
      }
    }
  }
</style>

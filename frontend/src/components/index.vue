<template>
    <div class="index">
      <site-header></site-header>
      <div class="body">
        <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
          <el-menu-item index="0" @click="gotoIndex">HOME</el-menu-item>
          <el-menu-item index="1" @click="gotoClassInfo('1')">游戏本</el-menu-item>
          <el-menu-item index="2" @click="gotoClassInfo('2')">轻薄本</el-menu-item>
          <el-menu-item index="3" @click="gotoClassInfo('3')">商务本</el-menu-item>
          <el-menu-item index="4" @click="gotoClassInfo('4')">台式机</el-menu-item>
        </el-menu>
        <div class="body-header">
          <el-carousel :interval="5000" height="600px">
            <el-carousel-item v-for="item in imageBox" :key="item.id">
              <img :src="item.idView" class="image">
            </el-carousel-item>
          </el-carousel>
        </div>

      </div>
    </div>
</template>

<script>
  import userInfo from './userInfo'
  import siteHeader from './siteHeader'

    export default {
        name: "index",
        components:{userInfo,siteHeader},
        mounted(){
          this.username = sessionStorage.getItem('username')
          this.userId = sessionStorage.getItem('userId')
          this.nickName = sessionStorage.getItem('nickName')
          if(!this.nickName)
            this.nickName = this.username
          this.email = sessionStorage.getItem('email')

        },
        data(){
            return{
              activeIndex:'0',
              imageBox:[
                {id:0,idView:require("../static/img/computer1.jpg")},
                {id:1,idView:require("../static/img/computer2.jpg")},
                {id:2,idView:require("../static/img/computer3.jpg")},
                {id:3,idView:require("../static/img/computer4.jpg")},
                {id:4,idView:require("../static/img/computer5.jpg")},
              ],
              username:null,
              nickName:'',
              userId:'',
              userInfoVisible:false,
              tableDataNew:[],
              tableDataHot:[]
            }
        },
      methods:{
        handleSelect(key, keyPath) {
          console.log(key, keyPath);
        },
        gotoClassInfo(classNum){
          this.$router.push({path:'/classInfo/'+classNum})
        },
        gotoIndex(){
          this.$router.push({name:'index'})
        },
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
    .body-header{
      margin-top:200px;
      z-index:-1;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: space-around;
      img{
        width:700px;
        height:700px;
        border-left:3px solid #ffecec;
        border-top:4px solid #ffecec;
        border-radius: 10px;
      }
      .el-carousel{
        width:45%;
      }
      .body-header-right{
        height:400px;
        width:45%;
        background-color: aliceblue;
        .el-tabs{
          height:395px;
        }
      }
    }
    .el-menu{
      position:fixed;
      left:0;
      top:100px;
      width:100%;
      li{
        font-size:17px;
      }
    }
  }
</style>

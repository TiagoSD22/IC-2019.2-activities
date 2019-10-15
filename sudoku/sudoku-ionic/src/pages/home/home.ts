import { Component } from '@angular/core';
import { NavController, LoadingController, ToastController } from 'ionic-angular';
import { SudokuProvider } from '../../providers/sudoku';


@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  isReady:boolean = false;
  initialSudoku = 
    [
      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],
      
      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],
      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

      [
        [0, 0, 0], 
        [0, 0, 0], 
        [0, 0, 0], 
      ],

    ]
  sudoku=null;

  constructor(
    private navCtrl: NavController,
    private sudokuProvider: SudokuProvider,
    private loadingController: LoadingController,
    private toastController: ToastController
    ) {

  }

  ionViewWillEnter(){
    this.sudoku = this.initialSudoku;
  }

  getRandomSudoku(){
    let loading = this.loadingController.create({
      content: 'Buscando o sudoku...',
      spinner: 'dots',
      cssClass: 'my-loading-class',
      duration: 5000

    })

    loading.present()
    .then(() => this.sudokuProvider.getSudoku())
    .then(resp=> this.sudoku =  resp['sudokuSelected'])
    .then(()=>{
      this.isReady = true
      
    })
    .catch(error =>{ 
      console.log(error);
      
      this.isReady = false;
      this.sudoku = this.initialSudoku;
      this.toastController.create({
        message: `Erro ao tentar carregar o sudoku!!`,
        duration: 3000,
        position: 'top'
      }).present()
    })
    //.then(() => loading.dismiss().catch(() => { }))
  }


 
  
  solveSudokuFromApi(sudoku){
    let loading = this.loadingController.create({
      content: 'Aplicando heuristica para resolver o sudoku... Não desligue seu computador, isso pode levar um tempo!',
      spinner: 'dots',
      cssClass: 'my-loading-class'
    })

    loading.present()
    .then(() => this.sudokuProvider.solveSudoku(sudoku))
    .then(resp=>{
      if(resp){
        this.sudoku =  resp;
        loading.dismiss()
      }
      
    })
    .catch(error => {
      console.log(error);
      //this.sudoku = this.initialSudoku;
      this.toastController.create({
        message: `Erro ao tentar resolver o sudoku!!`,
        duration: 5000,
        position: 'top'
      }).present()
    })
    //.catch(() => loading.dismiss())

  }
}
